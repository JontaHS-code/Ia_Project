document.getElementById("send-button").addEventListener("click", () => {
  const userInput = document.getElementById("user-input");
  const message = userInput.value;

  if (message.trim() === "") return;

  appendMessage("You", message);
  userInput.value = "";
  fetchChatResponse(message);
});

function appendMessage(sender, message) {
  const output = document.getElementById("output");
  const messageElement = document.createElement("div");
  messageElement.textContent = `${sender}: ${message}`;
  output.appendChild(messageElement);

  output.scrollTop = output.scrollHeight;
}

javascript;
function fetchChatResponse(message) {
  fetch("http://localhost:5000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ mensagem: message }),
  })
    .then((response) => response.json())
    .then((data) => {
      appendMessage("Bot", data.resposta.content); // Accessing the nested 'content'
    });
}
