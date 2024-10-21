from flask import request, Blueprint, jsonify, render_template
from API_PLAM import DB_HOST, DB_PATH, DB_USER, DB_PASS
import fdb

views = Blueprint('views', __name__)

@views.route('/')
def dashbord():
    return render_template('dashbord.html')

@views.route('/consulta', methods=['GET'])
def consulta():
    emp = request.args.get('emp')
    ben = request.args.get('ben')
    dep = request.args.get('dep')

    # Verificando os parâmetros obrigatórios
    if not emp or not ben or not dep:
        return jsonify({'error': 'Parâmetros "emp", "ben" e "dep" são obrigatórios.'}), 400

    try:
        with fdb.connect(
            dsn=f"{DB_HOST}:{DB_PATH}",
            user=DB_USER,
            password=DB_PASS
        ) as con:
            cur = con.cursor()

            # Executando a consulta fornecida
            cur.execute("""
                SELECT 
                    pf.emp,
                    pf.ben, 
                    pf.dep,
                    ps.nome AS cliente,
                    ps.cpf,
                    lpad(ps.emp, 6, '0') || lpad(ps.BEN, 6, '0') || lpad(ps.dep, 2, '0')  ||
                    CASE ps.PARENTE
                        WHEN 1 THEN '00' 
                        WHEN 3 THEN '01'  
                        WHEN 4 THEN '10' 
                        WHEN 5 THEN '30' 
                        WHEN 6 THEN '20'  
                        WHEN 7 THEN '20'  
                        WHEN 8 THEN '50'  
                        WHEN 9 THEN '50'  
                        WHEN 10 THEN '60' 
                        WHEN 12 THEN '60'
                        ELSE '--'
                    END || RIGHT(ps.cns, 1) AS MATRICULA,
                    p3.NOME AS CONTRATANTE,
                    (EXTRACT(DAY FROM pf.DATA_GUIA) || '/' || 
                     RIGHT('0' || EXTRACT(MONTH FROM pf.DATA_GUIA), 2) || '/' || 
                     EXTRACT(YEAR FROM pf.DATA_GUIA)) AS DATA_GUIA,
                    pfl.NOME_PROC AS PROCEDIMENTO,
                    REPLACE(pfl.VLR_TOTALFRQ, '.', ',') AS COPART_CLIENTE,
                    t2.nome AS SOLICITANTE, 
                    t.nome AS prestador,
                    pf.PLANO AS cod_plano, 
                    p.nome AS PLANO
                FROM PFLGUIAS pfl 
                JOIN PFGUIAS pf ON pfl.ID_PFGUIAS = pf.id  
                JOIN PSEMPBEN p3 ON p3.EMP = pf.EMP
                JOIN TBCREPLS t2 ON t2.COD = pf.SOLICITANTE
                JOIN TBCREPLS t ON t.COD = pf.PS 
                JOIN PSPLANOS p ON p.COD = pf.PLANO
                JOIN psbenefi ps ON ps.emp = pf.emp AND ps.ben = pf.ben AND ps.dep = pf.dep
                WHERE pf.emp = ? AND pf.ben = ? AND pf.dep = ?
                AND pf.status <> 'C' AND pfl.status <> 'C'
            """, (emp, ben, dep))

            results = cur.fetchall()

            # Processando os resultados da consulta
            processed_results = []
            for row in results:
                emp, ben, dep, cliente, cpf, matricula, contratante, data_guia, procedimento, copart_cliente, solicitante, prestador, cod_plano, plano = row

                # Decodificação se necessário
                if isinstance(cliente, bytes):
                    cliente = cliente.decode('latin1', errors='ignore')
                if isinstance(cpf, bytes):
                    cpf = cpf.decode('latin1', errors='ignore')

                processed_results.append({
                    "emp": emp,
                    "ben": ben,
                    "dep": dep,
                    "cliente": cliente,
                    "cpf": cpf,
                    "matricula": matricula,
                    "contratante": contratante,
                    "data_guia": data_guia,
                    "procedimento": procedimento,
                    "copart_cliente": copart_cliente,
                    "solicitante": solicitante,
                    "prestador": prestador,
                    "cod_plano": cod_plano,
                    "plano": plano
                })

            return jsonify(processed_results)

    except fdb.DatabaseError as db_error:
        error_message = str(db_error)
        return jsonify({'error': f'Erro ao consultar o banco de dados: {error_message}'}), 500

    except Exception as e:
        print(f"Erro: {str(e)}")
        return jsonify({'error': 'Erro inesperado ao processar a solicitação.'}), 500
