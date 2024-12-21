from flask import Flask, request, render_template
import csv
from twilio.rest import Client
import os
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
        
        # Ler os números do arquivo CSV
        contacts = []
        csv_reader = csv.reader(file.stream)
        for row in csv_reader:
            if row:
                contacts.append(row[0])

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
