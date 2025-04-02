// frontend/src/js/chat.js
const socket = new WebSocket(
  `ws://${window.location.host}/ws/chat/?token=${localStorage.getItem('access_token')}`
);

socket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  document.getElementById('chat-box').innerHTML += `<div>${data.message}</div>`;
};

// Автоматическое обновление токена
socket.onclose = async function(e) {
  if(e.code === 4001) {
    const newToken = await fetch('/auth/refresh/', {
      method: 'POST',
      body: JSON.stringify({refresh: localStorage.getItem('refresh_token')})
    });
    localStorage.setItem('access_token', newToken.access);
    connectWebSocket(); // Переподключение
  }
};