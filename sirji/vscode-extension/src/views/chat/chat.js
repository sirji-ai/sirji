const userInput = document.getElementById('userInput');
userInput.addEventListener('input', adjustTextAreaHeight);
userInput.addEventListener('paste', () => setTimeout(adjustTextAreaHeight, 0));
document.getElementById('sendBtn').addEventListener('click', sendUserMessage);

// IMP: Acquire the VS Code API
const vscode = acquireVsCodeApi();

// Listen for messages from the extension
window.addEventListener('message', (event) => {
 sendBotMessage(event.data);
});

function sendUserMessage() {
 const message = userInput.value.trim();
 if (message) {
  displayMessage(message, 'user');
  vscode.postMessage(message);
  userInput.value = '';
  adjustTextAreaHeight();
 }
}

function sendBotMessage(message) {
 message = message.trim();
 if (message) {
  displayMessage(message, 'bot');
  adjustTextAreaHeight();
 }
}

function adjustTextAreaHeight() {
 const minHeight = 15;
 const maxHeight = 90;

 userInput.style.height = minHeight + 'px';
 const newHeight = Math.min(maxHeight, Math.max(userInput.scrollHeight, minHeight));
 userInput.style.height = newHeight + 'px';
}

function displayMessage(msg, sender) {
 const messageContainer = document.getElementById('messageContainer');
 const messageDiv = document.createElement('div');

 // Directly assign msg to `textContent` to avoid interpreting msg as HTML
 messageDiv.textContent = msg; // Use textContent for security

 messageDiv.classList.add(sender); // Apply .user or .bot styling
 messageContainer.appendChild(messageDiv);

 // Replace new lines in the textContent with <br> by wrapping lines in HTML
 // This is a safe operation since we are controlling the HTML structure and not
 // directly including user input in the HTML.
 const formattedMessage = messageDiv.innerHTML.replace(/\n/g, '<br>');
 messageDiv.innerHTML = formattedMessage;

 // // Replace new line characters with HTML line break to properly display in HTML
 // const formattedMessage = msg.replace(/\n/g, '<br>');
 // messageDiv.innerHTML = formattedMessage; // Use the formatted message here

 // messageDiv.classList.add(sender); // Apply .user or .bot styling
 // messageContainer.appendChild(messageDiv);

 // Defer the scrolling a bit to ensure layout updates
 messageContainer.scrollTop = messageContainer.scrollHeight;
}
