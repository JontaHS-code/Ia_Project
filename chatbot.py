import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize the OpenAI client
client = openai.OpenAI(api_key="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")

# Create a chat completion request
def conversa(mensagem, Lista_mensagem=[]):
    Lista_mensagem.append(
        {"role": "user", "content": mensagem}
    )

    resposta = client.chat.completions.create(
        model="gpt-4",  # Make sure the model name is correct
        messages=Lista_mensagem
    )

    return resposta.choices[0].message.content # Access content directly

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    mensagem = data['mensagem']
    resposta = conversa(mensagem)
    return jsonify(resposta={'content': resposta})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
