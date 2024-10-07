from flask import Flask, request, jsonify, send_from_directory
import openai
from langchain_openai import ChatOpenAI  # Importação atualizada
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from dotenv import load_dotenv
import os

# Carregando variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializando o cliente OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Conectando ao banco de dados PostgreSQL
db = SQLDatabase.from_uri('DATABASE_URL')

# Inicializando o modelo OpenAI GPT-4 Mini
llm = ChatOpenAI(model_name="gpt-4")

# Configurando o toolkit e o agente do Langchain
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

# Inicializando o Flask
app = Flask(__name__)

# Rota para servir o arquivo HTML
@app.route('/')
def serve_html():
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

# Função para interagir com o modelo e o banco de dados
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    # Resposta do banco de dados se a mensagem solicitar interação
    try:
        # Verifica se a mensagem é sobre o banco de dados
        if any(keyword in user_message.lower() for keyword in [
            "mostrar", "exibir", "consultar", "banco de dados", "calendário", "encontros", "selecionar", "listar", "dados",
            "visualizar", "revelar", "apresentar", "disponibilizar", "obter", "recuperar", "trazer", "mostrar-me",
            "dar", "informar", "expor", "encontrar", "analisar", "investigar", "explorar", "exame", "revisar",
            "acessar", "listar", "sumário", "detalhes", "registro", "documento", "informações", "historico",
            "exibir informações", "apresentar dados", "procurar", "pesquisar", "aferir", "averiguar", "escavar"
        ]):
            response = agent_executor.run(user_message)
        else:
            # Para perguntas gerais, usa o modelo GPT-4
            response = llm.invoke(user_message)

        # Extraindo apenas o conteúdo da resposta
        response_content = response.content if hasattr(response, 'content') else response

    except Exception as e:
        response_content = f"Desculpe, ocorreu um erro ao processar sua mensagem: {str(e)}"
    
    return jsonify({"response": response_content})

# Iniciando o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
