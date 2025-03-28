// script.js

document.addEventListener("DOMContentLoaded", function () {
    const inputField = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const chatBox = document.getElementById("chat-box");
    const apiUrl = "http://127.0.0.1:8000/chat/";

    // Send message on button click
    sendBtn.addEventListener("click", sendMessage);

    // Send message when pressing Enter
    inputField.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        const userText = inputField.value.trim();
        if (userText === "") return;

        appendMessage("user", userText);
        inputField.value = "";

        // Show bot thinking message
        const botMessage = appendMessage("bot", "Thinking...");

        // Make API request
        fetch(apiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: "12345",
                prompt: userText,
                language: "en",
                url: null
            })
        })
        .then(response => response.json())
        .then(data => {
            botMessage.textContent = data.response || "No response received.";
        })
        .catch(error => {
            console.error("Error:", error);
            botMessage.textContent = "Error: Unable to reach backend.";
        });
    }

    function appendMessage(sender, text) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add(sender === "user" ? "user-message" : "bot-message");
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        return messageDiv;
    }
});
