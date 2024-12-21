from flask import Flask, request, render_template
import os
import csv
import pandas as pd
from twilio.rest import Client
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Inicializando o app Flask
app = Flask(__name__)

# Credenciais da Twilio (substitua pelas suas ou use .env)
account_sid = os.getenv("TWILIO_ACCOUNT_SID", "AC93bd21ec53faa0a2af9836c1bfe47894")
auth_token = os.getenv("TWILIO_AUTH_TOKEN", "8cbe0a522101cb6a96f2de0329682748")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER", "+12185035061")

# Cliente Twilio
client = Client(account_sid, auth_token)

# Função para processar arquivos CSV
def process_csv(file):
    contacts = []
    csv_file = csv.reader(file.stream.read().decode("utf-8").splitlines())
    for row in csv_file:
        if row:  # Ignora linhas vazias
            contacts.append(row[0])  # Adiciona o número da primeira coluna
    return contacts

# Função para processar arquivos XLSX
def process_xlsx(file):
    contacts = []
    df = pd.read_excel(file.stream)
    if 'phone' in df.columns:
        contacts = df['phone'].dropna().tolist()
    return contacts

# Função para processar arquivos TXT
def process_txt(file):
    contacts = []
    lines = file.read().decode("utf-8").splitlines()
    for line in lines:
        contacts.append(line.strip())  # Adiciona números linha por linha
    return contacts

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-messages', methods=['POST'])
def send_messages():
    try:
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return "Arquivo não encontrado!", 400
        
        file = request.files['file']
        message = request.form['message']
        
        # Verificar o tipo de arquivo
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[-1].lower()

        if file_extension == 'csv':
            contacts = process_csv(file)
        elif file_extension == 'xlsx':
            contacts = process_xlsx(file)
        elif file_extension == 'txt':
            contacts = process_txt(file)
        else:
            return "Formato de arquivo não suportado. Envie um CSV, XLSX ou TXT.", 400

        # Verifica se há números no arquivo
        if not contacts:
            return "Nenhum número encontrado no arquivo!", 400

        # Enviar mensagem para cada número
        for number in contacts:
            if number:
                client.messages.create(
                    body=message,
                    from_=twilio_number,
                    to=number
                )

        return "Mensagens enviadas com sucesso!"

    except Exception as e:
        return f"Ocorreu um erro: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
