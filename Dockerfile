# Usa uma imagem base do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o conteúdo do diretório atual para o diretório de trabalho do container
COPY . .

# Instala as dependências do projeto
RUN pip install -r requirements.txt

# Expõe a porta em que o Flask será executado
EXPOSE 8080

# Comando para iniciar a aplicação Flask
CMD ["gunicorn", "-b", "0.0.0.0:8080", "API_PLAM:app"]
