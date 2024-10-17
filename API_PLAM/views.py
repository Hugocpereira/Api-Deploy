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

    if not emp or not ben:
        return jsonify({'error': 'Parâmetros "emp" e "ben" são obrigatórios.'}), 400

    try:
        with fdb.connect(
            dsn=f"{DB_HOST}:{DB_PATH}",
            user=DB_USER,
            password=DB_PASS
        ) as con:
            cur = con.cursor()

            # Consulta dados eu acho (obs: lembrar de adicionar os parâmetros certos e testar)
            cur.execute("""
                SELECT
                    b.nome, -- Nome do cliente/empresa
                    b.cpf_cnpj, -- CPF ou CNPJ
                    p.tipo_plano, -- Tipo do plano (Master ou Ideal)
                    p.valor_mensalidade, -- Valor da mensalidade
                    h.historico -- Histórico de utilização
                FROM psbenefi b
                JOIN planos p ON b.plano_id = p.id
                LEFT JOIN historico h ON b.id = h.beneficiario_id
                WHERE b.emp = ? AND b.ben = ?
            """, (emp, ben))

            results = cur.fetchall()

            processed_results = []
            for row in results:
                nome, cpf_cnpj, tipo_plano, valor_mensalidade, historico = row

                if isinstance(nome, bytes):
                    nome = nome.decode('latin1', errors='ignore')
                if isinstance(cpf_cnpj, bytes):
                    cpf_cnpj = cpf_cnpj.decode('latin1', errors='ignore')

                processed_results.append({
                    "nome": nome,
                    "cpf_cnpj": cpf_cnpj,
                    "tipo_plano": tipo_plano,
                    "valor_mensalidade": valor_mensalidade,
                    "historico_utilizacao": historico
                })

            return jsonify(processed_results)

    except fdb.DatabaseError as db_error:
        error_message = str(db_error)
        return jsonify({'error': f'Erro ao consultar o banco de dados: {error_message}'}), 500

    except Exception as e:
        print(f"Erro: {str(e)}")
        return jsonify({'error': 'Erro inesperado ao processar a solicitação.'}), 500