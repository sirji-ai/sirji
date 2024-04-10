const BotSvg = `
<svg width="24" height="24" viewBox="0 0 300 300" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="300" height="300" fill="#3D3933"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M145.906 24.0177C137.403 26.5548 132.305 32.9899 132.305 41.188C132.305 47.7511 136.323 54.7205 142.136 58.2396C143.382 58.9946 144.559 59.2345 144.75 59.509C145.318 60.3215 145.462 83.6735 144.909 85.1216C144.274 86.7856 137.453 94.7265 130.019 102.456L128.663 103.866L124.98 100.013C122.954 97.8936 120.47 95.2434 119.459 94.1242C118.448 93.0044 116.823 91.8753 115.848 91.6155C114.653 91.2971 113.93 90.6045 113.632 89.494C113.077 87.4275 111.007 84.771 108.841 83.3464C105.292 81.014 99.5514 82.6161 96.2157 86.8697C95.0588 88.3451 94.7728 89.4699 94.7728 92.5486C94.7728 95.9644 94.9763 96.5994 96.6178 98.3073C97.6327 99.3628 99.2804 100.634 100.28 101.13C102.453 102.211 106.954 102.321 107.96 101.318C108.505 100.776 110.18 102.155 114.872 107.009L121.066 113.415L117.175 117.772C115.035 120.17 112.756 122.756 112.11 123.522C111.465 124.287 110.745 124.913 110.511 124.913C110.278 124.913 107.478 122.312 104.29 119.133C98.1947 113.054 93.122 109.145 90.4662 108.48C89.5934 108.262 88.8793 107.835 88.8793 107.532C88.8793 107.229 88.344 106.981 87.6901 106.981C86.8458 106.981 86.1801 106.144 85.396 104.098C83.4834 99.1056 80.8202 97.0873 76.147 97.0873C68.6468 97.0873 64.0573 105.549 68.0971 111.927C70.6276 115.923 75.3597 117.736 79.3313 116.231C80.8524 115.654 81.2476 115.809 83.1019 117.712C84.2415 118.881 86.3563 120.395 87.8018 121.077C90.3595 122.282 100.805 132.188 101.148 133.734C101.452 135.101 85.9599 150.158 76.4354 157.753C74.2375 159.506 72.3001 161.138 72.1295 161.379C71.7051 161.982 65.4053 166.342 64.9605 166.342C63.9568 166.342 60.3426 169.726 60.3426 170.666C60.3426 172.072 62.7024 177.469 63.927 178.864C65.4624 180.613 67.0499 180.271 71.8193 177.168C72.8429 176.501 73.9037 175.602 74.1767 175.169C74.4496 174.735 74.959 174.381 75.3088 174.381C76.1203 174.381 82.6757 169.298 82.6757 168.669C82.6757 168.41 83.0708 168.197 83.5547 168.197C84.038 168.197 84.5262 167.958 84.6404 167.665C84.7539 167.373 86.2428 165.946 87.9488 164.495C100.598 153.735 116.577 137.815 127.919 124.672C129.354 123.009 130.858 121.306 131.261 120.888C131.665 120.47 133.809 118.091 136.027 115.603C143.759 106.928 144.873 105.744 145.303 105.744C145.542 105.744 147.241 107.623 149.081 109.918C152.085 113.667 157.46 120.118 161.06 124.295C161.793 125.145 164.905 128.771 167.976 132.354C171.047 135.936 174.664 140.11 176.014 141.629C179.056 145.053 203.854 169.718 206.663 172.115C214.428 178.741 216.707 180.564 217.225 180.564C217.547 180.564 217.905 180.815 218.019 181.121C218.261 181.774 226.942 188.603 227.53 188.603C227.75 188.603 228.363 189.035 228.893 189.563C230.771 191.435 232.355 190.404 234.578 185.863C237.176 180.558 237.15 180.504 229.151 174.357C225.947 171.895 222.849 169.432 222.266 168.884C221.683 168.337 219.715 166.636 217.895 165.106C208.143 156.908 191.992 140.834 181.304 128.689C179.091 126.175 176.853 123.671 176.328 123.124C175.804 122.577 173.292 119.626 170.746 116.565C168.2 113.504 165.95 110.861 165.746 110.691C165.237 110.267 154.377 96.3577 153.766 95.3467C153.424 94.7815 157.75 90.1086 167.921 80.0524L182.568 65.5719L186.228 65.9535C189.255 66.2688 190.378 66.0969 192.735 64.9604C194.3 64.2048 195.582 63.2278 195.582 62.7894C195.582 62.3516 196.001 61.6467 196.513 61.2231C197.865 60.1039 197.743 54.3242 196.317 51.9868C192.027 44.9562 181.999 45.4836 178.456 52.9261C177.903 54.0886 177.033 55.0396 176.521 55.0396C176.011 55.0396 171.625 58.9371 166.774 63.7008C161.924 68.464 157.767 72.174 157.537 71.9453C157.307 71.7165 157.119 68.8245 157.119 65.5188V59.509L159.446 58.4251C162.238 57.1234 165.823 53.6353 167.759 50.3358C168.959 48.2916 169.172 47.0437 169.177 42.0543C169.182 37.2343 168.944 35.7304 167.854 33.6738C165.412 29.0702 161.827 26.2406 155.592 23.9942C151.897 22.6629 150.436 22.6666 145.906 24.0177ZM146.764 36.5763C142.72 39.0708 142.723 44.7218 146.769 47.4648C153.074 51.7395 161.06 45.2555 157.302 38.9131C155.223 35.4052 150.398 34.3354 146.764 36.5763ZM113.221 55.6468C110.972 56.6009 109.608 58.234 108.418 61.3981C107.477 63.9024 107.42 64.7322 108.045 66.8148C108.941 69.7928 112.575 73.5901 114.531 73.5901C115.824 73.5901 115.95 73.8757 115.982 76.8914C116.004 79.0223 116.43 80.8315 117.182 81.9928C118.376 83.838 122.39 87.804 123.068 87.809C123.913 87.8158 131.684 80.003 131.681 79.149C131.68 78.6426 130.909 77.3929 129.968 76.3726C126.472 72.5822 125.148 69.3037 126.722 68.3341C127.69 67.738 127.45 62.1067 126.361 59.8528C124.828 56.6826 122.638 55.4137 118.362 55.2208C116.306 55.128 113.993 55.3197 113.221 55.6468ZM76.1743 71.2941C70.8559 74.2962 69.4135 80.9379 73.0482 85.6874C76.137 89.724 80.4635 90.6472 85.1807 88.2758C88.1603 86.7782 90.7404 82.8325 90.7404 79.7736C90.7404 76.9502 88.1504 72.78 85.4673 71.2842C82.3115 69.5244 79.304 69.5275 76.1743 71.2941ZM214.503 71.419C213.48 71.8698 211.965 72.9606 211.138 73.8417C209.672 75.4043 209.434 75.4451 201.755 75.4451C197.421 75.4451 192.991 75.6213 191.911 75.8371C189.006 76.4159 180.308 85.3344 177.752 90.3554C175.301 95.1692 174.312 99.3109 175.212 100.987C175.927 102.319 177.618 104.315 182.312 109.368L185.482 112.78L185.933 105.256C186.438 96.8189 186.892 95.769 192.658 89.6801L195.598 86.5754H203.313C210.86 86.5754 211.089 86.6162 213.787 88.4304C215.4 89.5156 217.354 90.2855 218.495 90.2855C221.336 90.2855 225.085 88.1491 226.889 85.5025C232.223 77.6792 223.307 67.5408 214.503 71.419ZM200.618 96.4807C198.349 97.4435 195.616 100.892 195.48 102.962C195.133 108.274 196.387 111.868 199.001 113.056C200.132 113.569 200.421 114.365 200.756 117.9C200.976 120.227 201.158 124.54 201.161 127.483L201.165 132.837L204.418 135.522C206.206 136.999 208.37 138.921 209.226 139.794C211.484 142.096 218.913 147.792 219.657 147.792C220.007 147.792 220.386 148.022 220.5 148.303C220.7 148.797 231.643 156.465 234.708 158.259C239.387 160.997 241.413 161.446 242.586 160.004C243.708 158.625 245.291 153.141 244.954 151.801C244.685 150.73 237.164 145.152 231.63 141.918C230.388 141.192 225.19 137.184 224.739 136.604C224.569 136.385 222.335 134.534 219.776 132.492C211.794 126.122 212.332 127.075 212.332 119.302C212.332 114.527 212.591 112.095 213.203 111.133C214.438 109.191 214.946 105.165 214.253 102.813C213.929 101.712 212.718 99.8118 211.563 98.5918C209.702 96.6248 209.044 96.3434 205.78 96.1128C203.753 95.97 201.431 96.1357 200.618 96.4807ZM228.151 105.737C225.549 107.444 224.118 110.407 224.123 114.082C224.13 119.669 227.637 123.05 233.424 123.05C239.289 123.05 242.733 119.556 242.725 113.613C242.721 109.99 241.456 107.552 238.61 105.681C236.153 104.067 230.652 104.096 228.151 105.737ZM143.419 126.273C142.878 126.715 141.342 128.469 140.007 130.169C138.671 131.869 137.438 133.4 137.267 133.57C137.096 133.74 135.142 135.965 132.925 138.515C125.992 146.488 124.223 148.355 113.034 159.504C102.691 169.811 98.5818 173.58 93.1307 177.76C91.8161 178.767 90.7404 179.811 90.7404 180.078C90.7404 180.345 90.3452 180.564 89.8614 180.564C89.3781 180.564 88.8899 180.817 88.7757 181.127C88.4879 181.911 79.3629 188.362 75.3467 190.621C73.5191 191.65 71.8025 193.077 71.5327 193.793C70.9781 195.265 72.9577 199.687 75.2574 202.113C76.9807 203.931 79.1508 203.615 83.0771 200.974C84.5963 199.951 85.9909 199.115 86.1758 199.115C86.3613 199.115 87.1522 198.628 87.9345 198.033C88.7162 197.438 89.9736 196.533 90.7286 196.023C96.9013 191.851 111.199 179.71 119.187 171.857C124.394 166.739 137.283 152.944 139.29 150.342C140.371 148.94 141.475 147.792 141.743 147.792C142.011 147.792 142.231 147.404 142.231 146.931C142.231 146.22 143.46 145.319 144.429 145.319C144.819 145.319 147.126 147.911 149.758 151.305C152.169 154.415 152.209 154.543 151.114 155.686C150.493 156.333 148.869 158.21 147.504 159.858C142.83 165.499 139.468 169.132 132.323 176.26C121.169 187.387 116.847 191.076 103.392 200.949C98.3101 204.679 93.8112 208.022 93.3943 208.378C92.9775 208.733 91.4092 209.675 89.9098 210.47C83.8308 213.691 82.9641 214.858 84.283 218.043C85.7986 221.702 88.1299 224.467 89.6994 224.467C91.0922 224.467 100.801 219.16 101.183 218.19C101.297 217.902 101.649 217.665 101.965 217.665C103.163 217.665 121.419 203.961 128.125 198.027C133.091 193.634 150.292 176.347 153.416 172.611C154.941 170.786 156.468 168.977 156.809 168.59C166.458 157.646 169.101 154.172 168.509 153.217C167.888 152.216 165.397 149.377 162.989 146.927C161.952 145.873 159.44 143.075 157.406 140.711C155.372 138.347 153.289 135.958 152.777 135.403C152.265 134.847 150.73 133.044 149.365 131.395C144.167 125.118 144.491 125.397 143.419 126.273ZM63.6894 129.189C62.6298 129.452 61.033 130.197 60.1416 130.845C58.3673 132.135 56 136.527 56 138.53C56 140.718 57.8251 144.325 59.8252 146.091C61.5095 147.578 62.2626 147.792 65.8167 147.792C70.9192 147.792 73.4161 146.284 75.2195 142.112C75.9081 140.519 76.472 138.901 76.472 138.517C76.472 138.133 75.9081 136.514 75.2195 134.921C73.2368 130.335 68.5221 127.992 63.6894 129.189ZM174.73 166.806C173.415 168.422 172.122 169.837 171.857 169.952C171.591 170.067 171.078 170.711 170.717 171.384C170.137 172.463 171.151 173.68 179.314 181.687C190.173 192.343 193.444 195.383 198.063 199.12C199.94 200.638 201.615 202.056 201.786 202.272C202.255 202.863 212.947 210.425 215.507 211.976C216.741 212.725 218.158 213.337 218.656 213.337C219.842 213.337 221.738 211.132 223.059 208.214C224.936 204.07 224.914 204.028 218.185 199.099C216.16 197.616 214.224 196.094 213.883 195.718C213.542 195.34 211.867 193.951 210.161 192.629C208.455 191.307 206.605 189.791 206.05 189.26C205.495 188.728 203.546 187.042 201.717 185.511C197.819 182.25 189.037 173.968 183.194 168.043C180.93 165.748 178.637 163.869 178.099 163.869C177.561 163.869 176.045 165.19 174.73 166.806ZM199.728 218.129C199.58 218.384 198.988 220.541 198.413 222.921C196.019 232.836 192.687 239.365 187.453 244.398C182.774 248.897 180.065 250.059 174.179 250.092C168.846 250.122 166.76 249.385 163.223 246.219C159.214 242.632 156.905 241.87 150.51 242.021C147.272 242.098 144.434 242.423 144.202 242.744C143.774 243.337 141.97 244.653 136.765 248.165C134.093 249.969 133.449 250.129 128.853 250.129C124.771 250.129 123.31 249.852 120.907 248.621C116.18 246.201 111.415 241.065 108.669 235.432C107.885 233.822 107.069 232.506 106.856 232.506C106.447 232.506 99.1464 235.863 97.5644 236.778C96.0352 237.663 96.7394 240.71 99.5738 245.471C101.028 247.912 102.496 250.39 102.838 250.977C106.911 257.984 118.224 267.963 126.256 271.635C127.536 272.22 129.49 273.109 130.599 273.612C132.498 274.472 134.872 275.133 140.68 276.422C142.045 276.725 146.947 276.985 151.575 277C159.639 277.026 166.652 275.935 171.078 273.968C177.219 271.238 181.399 269.085 183.459 267.592C188.274 264.101 198.055 254.37 198.06 253.066C198.062 252.641 198.298 252.293 198.584 252.293C198.871 252.293 199.432 251.667 199.832 250.902C200.231 250.136 201.097 248.675 201.757 247.655C202.415 246.635 203.68 244.27 204.566 242.399C205.451 240.529 206.445 238.515 206.773 237.924C207.532 236.556 211.024 226.828 211.084 225.911C211.088 225.855 209.651 224.755 207.889 223.467C206.129 222.179 203.834 220.346 202.789 219.395C200.819 217.602 200.187 217.34 199.728 218.129Z" fill="white"/>
</svg>
`;

const UserSvg = `
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 256 256"><path d="M230.92 212c-15.23-26.33-38.7-45.21-66.09-54.16a72 72 0 1 0-73.66 0c-27.39 8.94-50.86 27.82-66.09 54.16a8 8 0 1 0 13.85 8c18.84-32.56 52.14-52 89.07-52s70.23 19.44 89.07 52a8 8 0 1 0 13.85-8M72 96a56 56 0 1 1 56 56 56.06 56.06 0 0 1-56-56" fill="#fff"/></svg>
`;

const loaderSvg = `
  <svg id="dots" width="25px" height="22px" viewBox="0 0 132 58" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns">
    <defs></defs>
    <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" sketch:type="MSPage">
        <g id="dots" sketch:type="MSArtboardGroup" fill="#A3A3A3">
            <circle id="dot1" sketch:type="MSShapeGroup" cx="25" cy="30" r="13"></circle>
            <circle id="dot2" sketch:type="MSShapeGroup" cx="65" cy="30" r="13"></circle>
            <circle id="dot3" sketch:type="MSShapeGroup" cx="105" cy="30" r="13"></circle>
        </g>
    </g>
  </svg>
`;

let stepsArray = [];
let totalStepsCompleted = 0;
let coderTabInterval;
let plannerTabInterval;
let researcherTabInterval;

const userInput = document.getElementById('userInput');
userInput.addEventListener('keydown', onInputChange);
userInput.addEventListener('paste', () => setTimeout(adjustTextAreaHeight, 0));
document.getElementById('sendBtn').addEventListener('click', sendUserMessage);

// Settings modal
document.getElementById('saveSettings').onclick = function () {
  saveSettings();
};
document.getElementById('openSettings').onclick = function () {
  openSettings();
};
document.getElementById('closeSettings').onclick = function () {
  closeSettings();
};

// Planner modal
document.getElementById('progressCircle').addEventListener('click', () => {
  document.getElementById('plannerModal').style.display = 'flex';
});

document.getElementById('closePlanner').addEventListener('click', () => {
  document.getElementById('plannerModal').style.display = 'none';
});

// IMP: Acquire the VS Code API
const vscode = acquireVsCodeApi();

// Listen for messages from the extension
window.addEventListener('message', (event) => {
  console.log(`Received message in chat.js: ${event.data.type}`, event.data);
  switch (event.data.type) {
    case 'settingSaved':
      settingSaved(event.data.content.message);
      disableSendButton(!event.data.content.allowUserMessage);
      break;

    case 'botMessage':
      sendBotMessage(event.data.content.message, event.data.content.allowUserMessage);
      disableSendButton(!event.data.content.allowUserMessage, event.data.content.messageInputText);
      break;

    case 'plannedSteps':
      totalStepsCompleted = 0;
      displayPlannedSteps(event.data.content);
      break;

    case 'plannedStepStart':
      updateStepStatus(event.data.content, 'started');
      break;

    case 'plannedStepComplete':
      updateStepStatus(event.data.content, 'completed');
      break;

    case 'solutionCompleted':
      sendBotMessage(event.data.content.message, event.data.content.allowUserMessage);
      disableSendButton(!event.data.content.allowUserMessage);
      removRecentUserLoader();
      markSolutionCompleted(event.data.content);
      break;

    case 'tokenUsed':
      displayTokenUsed(event.data.content.message);
      break;

    case 'showCoderTab':
      displayCoderTab(event.data.content);
      break;

    case 'showPlannerTab':
      displayPlannerTab(event.data.content);
      break;

    case 'showResearcherTab':
      displayResearcherTab(event.data.content);
      break;

    case 'plannerLogs':
      displayPlannerLogs(event.data.content);
      break;

    case 'researcherLogs':
      displayResearcherLogs(event.data.content);
      break;

    case 'coderLogs':
      displayCoderLogs(event.data.content);
      break;

    default:
      sendBotMessage(`Unknown message received from facilitator: ${event.data}`, false);
  }
});

function updateIconColors() {
  const isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;

  const iconColor = isDarkMode ? '#FFFFFF' : '#000000';

  document.querySelectorAll('.icon').forEach((iconElement) => {
    iconElement.style.color = iconColor;
  });
}

function sendUserMessage() {
  const message = userInput.value.trim();
  if (message) {
    displayMessage(message, 'user');
    vscode.postMessage({ type: 'userMessage', content: message });
    userInput.value = '';
    adjustTextAreaHeight();
  }
  disableSendButton(true);
}

function sendBotMessage(message, allowUserInput) {
  message = message.trim();
  if (message) {
    displayMessage(message, 'bot', allowUserInput);
    adjustTextAreaHeight();
  }
}

function onInputChange(event) {
  removRecentUserLoader();
  adjustTextAreaHeight();
  
  // Check if "Command" key (Mac) or "Ctrl" key (Windows/Linux) and "Enter" key are pressed
  if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') {
    sendUserMessage();
  }
}

function adjustTextAreaHeight() {
  const minHeight = 15;
  const maxHeight = 90;

  userInput.style.height = minHeight + 'px';
  const newHeight = Math.min(maxHeight, Math.max(userInput.scrollHeight, minHeight));
  userInput.style.height = newHeight + 'px';
}

function displayMessage(msg, sender, allowUserInput) {
  const chatListContainerElement = document.getElementById('messageContainer');

  const messageElement = createMessageElement(msg, sender, allowUserInput);

  userInput.value = '';

  // Defer the scrolling a bit to ensure layout updates
  chatListContainerElement.appendChild(messageElement);

  if (sender === "bot" && allowUserInput) {
    displayMessage("Waiting for your input", "user", true); 
  }

  chatListContainerElement.scrollTop = chatListContainerElement.scrollHeight + 10;
}

function removRecentUserLoader() {
  const userMessages = document.querySelectorAll(".user-input-waiting");

  if (userMessages.length <= 0) {
    return;
  }

  const recentMessage = userMessages[userMessages.length - 1];

  recentMessage.remove();
}

function createMessageElement(msg, sender, allowUserInput) {
  removeAllLoaderInstanceFromDOM("message-loader");
  
  const chatElement = document.createElement('div');


  // Construct user message HTML format
  if (sender === 'user') {
    if (allowUserInput) {
      const loaderElement = document.createElement('div');
      loaderElement.classList.add('message-loader');
      loaderElement.innerHTML = loaderSvg;
      chatElement.appendChild(loaderElement);
    }

    const messageElement = document.createElement('div');
    if (allowUserInput) {
      messageElement.classList.add('user-text-inactive');
      chatElement.classList.add('user-message', 'user-input-waiting');
    } else {
      messageElement.classList.add('user');
      chatElement.classList.add('user-message');
    }
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
    iconElement.classList.add('boticon');
    iconElement.innerHTML = BotSvg;
    chatElement.appendChild(iconElement);

    const messageElement = document.createElement('div');
    messageElement.classList.add('bot');
    messageElement.textContent = msg;
    chatElement.appendChild(messageElement);
    const formattedMessage = messageElement.innerHTML.replace(/\n/g, '<br>');
    messageElement.innerHTML = formattedMessage;

    if (!allowUserInput) {
      const loaderElement = document.createElement('div');
      loaderElement.classList.add('message-loader');
      loaderElement.innerHTML = loaderSvg;
      chatElement.appendChild(loaderElement);
    }
  }
  
  return chatElement;
}

function removeAllLoaderInstanceFromDOM(className) {
  var elementsToRemove = document.querySelectorAll(`.${className}`);

  // Iterate over the NodeList and remove each element
  elementsToRemove.forEach(function (element) {
    element.remove();
  });
}

function openSettings() {
  document.getElementById('settingsModal').style.display = 'flex';
  //  vscode.postMessage({ type: 'requestEnvVariables' });
}

function closeSettings() {
  document.getElementById('settingsModal').style.display = 'none';
}

function saveSettings() {
  const openAIKey = document.getElementById('SIRJI_OPENAI_API_KEY').value.trim();

  let isValid = true;

  document.getElementById('save_settings_error').textContent = '';

  if (!openAIKey) {
    document.getElementById('SIRJI_OPENAI_API_KEY_ERROR').textContent = 'OpenAI API Key is required.';
    isValid = false;
  } else {
    document.getElementById('SIRJI_OPENAI_API_KEY_ERROR').textContent = '';
  }

  if (isValid) {
    const saveButton = document.getElementById('saveSettings');
    saveButton.textContent = 'Saving...';
    saveButton.disabled = true;

    const settings = {
      SIRJI_OPENAI_API_KEY: openAIKey,
    };

    vscode.postMessage({ type: 'saveSettings', content: settings });
  }
}

function settingSaved(data) {
  const saveButton = document.getElementById('saveSettings');
  saveButton.textContent = 'Save';
  saveButton.disabled = false;
  if (data.success) {
    sendBotMessage(data.message, false);
    closeSettings();
  } else {
    document.getElementById('save_settings_error').textContent = `Settings can not be saved. Please contact Sirji team. Error: ${data.message}`;
  }
}

function updateStepStatus(message, status) {
  let stepNumber = message.match(/\d+/g);

  if (!stepNumber) {
    return;
  }

  if (stepNumber && stepNumber.length === 0) {
    return;
  }

  if (stepsArray?.length === 0 || !stepsArray) {
    return;
  }

  if (stepNumber.length === 1) {
    console.log('Updating step:', stepNumber[0], stepsArray[0]);
    stepsArray[stepNumber[0] - 1].status = status;
    if (status === 'completed') {
      for (let i = 0; i < stepNumber[0] - 1; i++) {
        stepsArray[i].status = status;
      }
    }
  }

  let maxStepNumber = 0;
  if (stepNumber.length === 2) {
    maxStepNumber = Math.max(...stepNumber);
    for (let i = 0; i < maxStepNumber - 1; i++) {
      stepsArray[i].status = status;
    }
  }

  if (status === 'completed') {
    totalStepsCompleted = stepsArray.length;
    setProgress(totalStepsCompleted, stepsArray.length);

    toggleProgressTextColor();
  }

  totalStepsCompleted = stepsArray.filter((step) => step.status === 'completed').length;

  displayPlannedSteps(stepsArray);
}

function displayPlannedSteps(steps) {
  setProgress(totalStepsCompleted, steps.length);
  document.getElementById('progressCircle').style.visibility = 'visible';
  stepsArray = steps;
  const listElement = document.getElementById('plannerStepsList');
  listElement.innerHTML = '';

  if (!steps) {
    return;
  }

  if (steps.length === 0) {
    return;
  }

  steps.forEach((step, index) => {
    step.status = step.status || '';
    const listItem = document.createElement('li');
    listItem.className = 'stepItem';
    const stepDescription = step.description;

    if (step.status === 'started') {
      listItem.innerHTML = `<div class="loader"></div><label>${stepDescription}</label>`;
    } else {
      listItem.innerHTML = `
      <input type="checkbox" class="checkbox" id="checkbox-${index}" ${step.status === 'completed' ? 'checked' : ''}>
      <label for="checkbox-${index}">${stepDescription}</label>
      `;
    }
    listElement.appendChild(listItem);
  });
}

function setProgress(x, y) {
  const progressText = document.getElementById('progressText');
  progressText.textContent = `${x} of ${y} tasks done`;

  const progressTextInsideModal = document.getElementById('progressTextInsideModal');
  progressTextInsideModal.textContent = `${x} of ${y} tasks done`;
}

function disableSendButton(disable, message) {
  const sendButton = document.getElementById('sendBtn');
  if (sendButton) {
    sendButton.disabled = disable;
    updatePlaceholder(disable, message);
  }
}

function updatePlaceholder(disable, message) {
  const placeholderText = disable ? message || 'Sirji> is working on the problem. We will open the chat window when we have some information, questions, or feedback..' : 'Type a message...';
  userInput.placeholder = placeholderText;
  userInput.disabled = disable;

  adjustTextAreaHeight();
}

function markSolutionCompleted() {
  if (stepsArray?.length === 0) {
    return;
  }

  stepsArray.forEach((step) => {
    step.status = 'completed';
  });
  totalStepsCompleted = stepsArray.length;
  setProgress(stepsArray.length, stepsArray.length);
  displayPlannedSteps(stepsArray);
}

function toggleProgressTextColor() {
  // Select the element with id "progressText"
  const progressText = document.getElementById('progressText');

  // Update the background color
  progressText.style.backgroundColor = '#78a866';

  setTimeout(() => {
    progressText.style.backgroundColor = 'transparent';
  }, 2000);
}

function convertNumber(number) {
  if (number >= 1000000) {
      return (Math.ceil(number / 100000) / 10).toFixed(1).replace('.0', '') + 'M';
  } else if (number >= 100000) {
      return (Math.ceil(number / 10000) / 100).toFixed(1).replace('.0', '') + 'M';
  } else if (number >= 1000) {
      return (Math.ceil(number / 1000)).toFixed(1).replace('.0', '') + 'K';
  } else {
      return ""; // Don't show tokens less than 1K
  }
}

function displayTokenUsed(data = {}) {
  const { total_completion_tokens = 0, total_completion_tokens_value = 0, total_prompt_tokens = 0, total_prompt_tokens_value = 0 } = data;

  const totalTokensUsed = total_completion_tokens + total_prompt_tokens;

  if (totalTokensUsed < 1000) {
    return;
  }

  updateTokensUsed(totalTokensUsed);

  updateTooltipTokenValues(data);
}

function updateTokensUsed(totalTokensUsed) {
  const tokens = convertNumber(totalTokensUsed);

  const jTokensUsed = document.getElementById('jTokensUsed');
  jTokensUsed.textContent = `${tokens} tokens`;

  document.getElementById('jTokensContainer').style.display = 'flex';
}

function updateTooltipTokenValues(tokenValues) {
  const { total_completion_tokens = 0, total_completion_tokens_value = 0, total_prompt_tokens = 0, total_prompt_tokens_value = 0 } = tokenValues;

  const jPromptTokensUsed = document.getElementById('jPromptTokensUsed');
  jPromptTokensUsed.textContent = `Prompt Tokens - ${total_prompt_tokens} | $${total_prompt_tokens_value.toFixed(2)}`;

  const jCompletionTokensUsed = document.getElementById('jCompletionTokensUsed');
  jCompletionTokensUsed.textContent = `Completion Tokens - ${total_completion_tokens} | $${total_completion_tokens_value.toFixed(2)}`;
}

function displayPlannerLogs(data) {
  const plannerLogs = document.getElementById('plannerLogs');
  plannerLogs.innerText = data;
}

function displayResearcherLogs(data) {
  const researcherLogs = document.getElementById('researcherLogs');
  researcherLogs.innerText = data;
}

function displayCoderLogs(data) {
  const coderLogs = document.getElementById('coderLogs');
  coderLogs.innerText = data;
}

function displayCoderTab(data) {
  // showTab("coderTab");
  const coderTab = document.getElementById('coderTab');
  // coderTab.innerHTML = data;

  coderTabInterval = setInterval(() => {
    vscode.postMessage({ type: 'requestCoderLogs' });
  }, 10000);
}

function displayPlannerTab(data) {
  // showTab("plannerTab");
  const plannerTab = document.getElementById('plannerTab');
  // plannerTab.innerHTML = data;

  plannerTabInterval = setInterval(() => {
    vscode.postMessage({ type: 'requestPlannerLogs' });
  }, 10000);
}

function displayResearcherTab(data) {
  // showTab("researcherTab");
  const researcherTab = document.getElementById('researcherTab');
  // researcherTab.innerHTML = data;

  researcherTabInterval = setInterval(() => {
    vscode.postMessage({ type: 'requestResearcherLogs' });
  }, 10000);
}

function closeCoderTab() {
  clearInterval(coderTabInterval);
  document.getElementById('coderTab').innerHTML = '';
}

function closePlannerTab() {
  clearInterval(plannerTabInterval);
  document.getElementById('plannerTab').innerHTML = '';
}

function closeResearcherTab() {
  clearInterval(researcherTabInterval);
  document.getElementById('researcherTab').innerHTML = '';
}

const tabButtons = document.querySelectorAll('.tab-button');

tabButtons.forEach(function (button) {
  button.addEventListener('click', function () {
    const tabName = this.getAttribute('data-tab');
    showTab(tabName);
  });
});

function showTab(tabName) {
  let i, tabcontent, tablinks;

  // Get all elements with class="tab" and hide them
  tabcontent = document.getElementsByClassName('tab');
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = 'none';
  }

  // Get all elements with class="tab-button" and remove the class "active"
  tablinks = document.getElementsByClassName('tab-button');
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].classList.remove('active');
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = 'block';
  document.querySelector('[data-tab="' + tabName + '"]').classList.add('active');
}

// Show the initial tab on page load
showTab('chatTerminalTab');


updateIconColors();

vscode.postMessage({
  type: 'webViewReady',
  content: true,
});
