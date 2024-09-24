from flask import Flask, request, jsonify, send_from_directory
import openai

app = Flask(__name__)

# Inicialize o cliente OpenAI
client = openai.OpenAI(api_key="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")

# Rota para servir o arquivo HTML
@app.route('/')
def serve_html():
    return send_from_directory('.', 'chat.html')

# Rota específica para servir chat.html
@app.route('/chat.html')
def serve_chat_html():
    return send_from_directory('.', 'chat.html')

# Rota para servir o arquivo CSS
@app.route('/styles.css')
def serve_css():
    return send_from_directory('.', 'styles.css')

# Rota para servir o arquivo JavaScript
@app.route('/script.js')
def serve_js():
    return send_from_directory('.', 'script.js')

# Rota para servir a logo
@app.route('/Logos/<path:filename>')
def serve_logos(filename):
    return send_from_directory('Logos', filename)

# Função para criar uma solicitação de conclusão de chat
def conversa(mensagem, Lista_mensagem=[]):
    Lista_mensagem.append(
        {"role": "user", "content": mensagem}
    )

    resposta = client.chat.completions.create(
        model="gpt-4",  # Certifique-se de que o nome do modelo está correto
        messages=Lista_mensagem
    )

    return resposta.choices[0].message.content  # Acesse o conteúdo diretamente

# Rota para processar mensagens
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    # Chama a função conversa
    bot_response = conversa(user_message)
    return jsonify({"response": bot_response})  # Retorna a resposta em formato JSON

if __name__ == '__main__':
    app.run(debug=True)  # Inicia o servidor Flask
