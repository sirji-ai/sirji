import UserSvg from '../../assets/user_svg.js';
import BotSvg from '../../assets/bot_svg.js';
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

function updateIconColors() {
 const isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;

 const iconColor = isDarkMode ? '#FFFFFF' : '#000000'; // White for dark mode, black for light mode

 document.querySelectorAll('.icon').forEach((iconElement) => {
  iconElement.style.color = iconColor;
 });
}

updateIconColors();

function sendBotMessage(message) {
 message = message.trim();
 if (message) {
  displayMessage(message, 'bot');
  adjustTextAreaHeight();
 }
}

sendBotMessage('Hello, I am Sirji. What would you like me to build today?');

function adjustTextAreaHeight() {
 const minHeight = 15;
 const maxHeight = 90;

 userInput.style.height = minHeight + 'px';
 const newHeight = Math.min(maxHeight, Math.max(userInput.scrollHeight, minHeight));
 userInput.style.height = newHeight + 'px';
}

function displayMessage(msg, sender) {
 //  const messageContainer = document.getElementById('messageContainer');
 //  const messageDiv = document.createElement('div');

 const chatListContainerElement = document.getElementById('messageContainer');

 const messageElement = createMessageElement(msg, sender);

 // Defer the scrolling a bit to ensure layout updates
 chatListContainerElement.appendChild(messageElement);

 chatListContainerElement.scrollTop = chatListContainerElement.scrollHeight;

 userInput.value = '';
}

function createMessageElement(msg, sender) {
 const chatElement = document.createElement('div');

 // Construct user message HTML format
 if (sender === 'user') {
  chatElement.classList.add('user-message');
  const messageElement = document.createElement('div');
  messageElement.classList.add('user');
  messageElement.textContent = msg;

  chatElement.appendChild(messageElement);
  // Replace new line characters with HTML line break to properly display in HTML
  const formattedMessage = messageElement.innerHTML.replace(/\n/g, '<br>');
  messageElement.innerHTML = formattedMessage;

  const iconElement = document.createElement('div');
  iconElement.classList.add('icon');
  iconElement.innerHTML = UserSvg;
  chatElement.appendChild(iconElement);
 }

 // Construct bot message HTML format
 if (sender === 'bot') {
  chatElement.classList.add('bot-message');
  const iconElement = document.createElement('div');
  iconElement.classList.add('icon');
  iconElement.innerHTML = BotSvg;
  chatElement.appendChild(iconElement);

  const messageElement = document.createElement('div');
  messageElement.classList.add('bot');
  messageElement.textContent = msg;
  chatElement.appendChild(messageElement);
  const formattedMessage = messageElement.innerHTML.replace(/\n/g, '<br>');
  messageElement.innerHTML = formattedMessage;
 }

 return chatElement;
}
