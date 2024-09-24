document.getElementById("send-btn").addEventListener("click", function () {
  enviarMensagem(); // Chama a função para enviar a mensagem
});

// Adiciona o evento para enviar a mensagem ao pressionar Enter
document
  .getElementById("user-input")
  .addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      event.preventDefault(); // Impede o comportamento padrão do Enter (nova linha)
      enviarMensagem(); // Chama a função para enviar a mensagem
    }
  });

// Função para enviar a mensagem
function enviarMensagem() {
  const userInput = document.getElementById("user-input");
  const message = userInput.value;
  if (message) {
    addMessage("user", message); // Adiciona a mensagem do usuário
    userInput.value = ""; // Limpa o campo de entrada

    // Exibe os três pontos enquanto o bot está "pensando"
    addLoadingDots();

    fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Remove a mensagem de carregamento antes de adicionar a resposta
        removeLastMessage();
        addMessage("bot", data.response); // Adiciona a resposta do bot
      });
  }
}

// Função para adicionar mensagens ao chat
function addMessage(role, content) {
  const chatBox = document.getElementById("chat");
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message");

  // Define a classe baseada no papel (usuário ou bot)
  if (role === "user") {
    messageDiv.classList.add("user-message");

    // Adiciona o ícone do usuário
    const userIcon = document.createElement("img");
    userIcon.src = "Logos/user.png"; // Caminho para o ícone do usuário
    userIcon.alt = "Usuário";
    userIcon.classList.add("message-icon"); // Adiciona classe para estilização
    messageDiv.appendChild(userIcon); // Adiciona o ícone ao messageDiv
  } else {
    messageDiv.classList.add("bot-message");

    // Adiciona o ícone do bot
    const botIcon = document.createElement("img");
    botIcon.src = "Logos/logo_ia1.png"; // Caminho para o ícone do bot
    botIcon.alt = "Bot";
    botIcon.classList.add("message-icon"); // Adiciona classe para estilização
    messageDiv.appendChild(botIcon); // Adiciona o ícone ao messageDiv
  }

  // Adiciona o conteúdo da mensagem
  const textNode = document.createElement("span");
  textNode.textContent = content;
  messageDiv.appendChild(textNode);

  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight; // Rola para a última mensagem
}

// Função para exibir os três pontos enquanto o bot está "pensando"
function addLoadingDots() {
  const chatBox = document.getElementById("chat");
  const loadingDiv = document.createElement("div");
  loadingDiv.classList.add("message", "bot-message");

  const botIcon = document.createElement("img");
  botIcon.src = "Logos/logo_ia1.png"; // Caminho para o ícone do bot
  botIcon.alt = "Bot";
  botIcon.classList.add("message-icon");
  loadingDiv.appendChild(botIcon);

  const loadingText = document.createElement("span");
  loadingText.textContent = "...";
  loadingDiv.appendChild(loadingText);

  chatBox.appendChild(loadingDiv);
  chatBox.scrollTop = chatBox.scrollHeight; // Rola para a última mensagem

  // Alterna os pontos
  let dotCount = 0;
  const interval = setInterval(() => {
    dotCount = (dotCount + 1) % 4;
    loadingText.textContent = ".".repeat(dotCount); // Atualiza os pontos
  }, 500);

  // Limpa o intervalo após a resposta do bot
  return interval;
}

// Função para remover a última mensagem (carregando)
function removeLastMessage() {
  const chatBox = document.getElementById("chat");
  if (
    chatBox.lastChild &&
    chatBox.lastChild.classList.contains("bot-message")
  ) {
    chatBox.removeChild(chatBox.lastChild);
  }
}

// Função para iniciar um novo chat
function iniciarNovoChat() {
  const chatBox = document.getElementById("chat");
  chatBox.innerHTML = ""; // Limpa todas as mensagens
  addMessage("bot", "Bem-vindo ao chat! Como posso ajudar você hoje?"); // Mensagem de boas-vindas
}

// Adiciona evento ao botão de novo chat
document
  .getElementById("new-chat-btn")
  .addEventListener("click", iniciarNovoChat);

// Mensagem de boas-vindas ao entrar no chat
window.onload = function () {
  iniciarNovoChat();
};
