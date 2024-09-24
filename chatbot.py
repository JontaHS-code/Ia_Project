import openai
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


if __name__ == '__main__':
    lista_mensagem = []
    while True:
        mensagem_user = input("Você: ")
        if mensagem_user.lower() in ["bye", 'tchau', 'até mais', 'exit', 'sair']:
            print("Resposta: Tchau, até mais! Sinta-se à vontade para voltar e conversar mais!")
            break
        else:
            resposta = conversa(mensagem_user, lista_mensagem)

        print('Resposta: ', resposta)
        print()
