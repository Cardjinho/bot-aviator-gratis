from flask import Flask, request
import csv
from twilio.rest import Client

app = Flask(__name__)

# Credenciais da Twilio (Substitua pelos seus dados)
account_sid = "AC93bd21ec53faa0a2af9836c1bfe47894"
auth_token = "8cbe0a522101cb6a96f2de0329682748"
twilio_number = "+12185035061"  # Seu número Twilio

client = Client(account_sid, auth_token)

@app.route('/')
def home():
    return open("index.html").read()

@app.route('/send-messages', methods=['POST'])
def send_messages():
    try:
        # Obter o arquivo CSV e a mensagem
        file = request.files['file']
        message = request.form['message']
        
        # Ler números do arquivo CSV
        contacts = []
        csv_reader = csv.reader(file.stream)
        for row in csv_reader:
            contacts.append(row[0])  # Assume que os números estão na primeira coluna
        
        # Enviar mensagens
        for number in contacts:
            if number:  # Se o número não estiver vazio
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
