const socket = io();

const nameScreen = document.getElementById('name-screen');
const chatScreen = document.getElementById('chat-screen');
const nameForm = document.getElementById('name-form');
const chatForm = document.getElementById('chat-form');
const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const userNameDisplay = document.getElementById('user-name');

let username = '';

nameForm.addEventListener('submit', (e) => {
    e.preventDefault();
    username = document.getElementById('name-input').value.trim();
    if (username) {
        nameScreen.classList.add('hidden');
        chatScreen.classList.remove('hidden');
        userNameDisplay.textContent = `Logged in as: ${username}`;
        socket.emit('join', { username });
    }
});

chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = messageInput.value.trim();
    if (message) {
        socket.emit('send_message', { username, message }, (response) => {
            if (response && response.status !== 'ok') {
                console.error('Failed to send message:', response.message);
            }
        });
        messageInput.value = '';
    }
});

socket.on('new_message', (data) => {
    addMessageToChat(data);
});

socket.on('user_joined', (data) => {
    addSystemMessage(`${data.username} has joined the chat`);
});

socket.on('user_left', (data) => {
    addSystemMessage(`${data.username} has left the chat`);
});

socket.on('message_updated', (data) => {
    const messageElement = document.getElementById(`message-${data.id}`);
    if (messageElement) {
        messageElement.querySelector('p').textContent = data.message;
    }
});

socket.on('message_deleted', (data) => {
    const messageElement = document.getElementById(`message-${data.id}`);
    if (messageElement) {
        messageElement.remove();
    }
});

function addMessageToChat(data) {
    const messageElement = document.createElement('div');
    messageElement.id = `message-${data.id}`;
    messageElement.classList.add('message', data.username === username ? 'own' : 'other');
    
    const messageContent = `
        <div class="message-header">
            <span class="username">${data.username}</span>
            <span class="timestamp">${data.timestamp}</span>
        </div>
        <p>${data.message}</p>
    `;
    
    messageElement.innerHTML = messageContent;
    
    if (data.username === username) {
        const actionsDiv = document.createElement('div');
        actionsDiv.classList.add('message-actions');
        
        const editButton = document.createElement('button');
        editButton.innerHTML = '<i class="fas fa-edit"></i>';
        editButton.addEventListener('click', () => editMessage(data.id));
        
        const deleteButton = document.createElement('button');
        deleteButton.innerHTML = '<i class="fas fa-trash-alt"></i>';
        deleteButton.addEventListener('click', () => deleteMessage(data.id));
        
        actionsDiv.appendChild(editButton);
        actionsDiv.appendChild(deleteButton);
        messageElement.appendChild(actionsDiv);
    }
    
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addSystemMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'system');
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function editMessage(messageId) {
    const messageElement = document.getElementById(`message-${messageId}`);
    const messageText = messageElement.querySelector('p');
    const newText = prompt('Edit your message:', messageText.textContent);
    if (newText !== null && newText.trim() !== '') {
        socket.emit('update_message', { id: messageId, message: newText }, (response) => {
            if (response && response.status !== 'ok') {
                console.error('Failed to update message:', response.message);
            }
        });
    }
}

function deleteMessage(messageId) {
    if (confirm('Are you sure you want to delete this message?')) {
        socket.emit('delete_message', { id: messageId }, (response) => {
            if (response && response.status !== 'ok') {
                console.error('Failed to delete message:', response.message);
            }
        });
    }
}

socket.on('connect_error', (error) => {
    console.error('Connection error:', error);
    addSystemMessage('Connection error. Please try refreshing the page.');
});

socket.on('disconnect', (reason) => {
    console.log('Disconnected:', reason);
    addSystemMessage('Disconnected from server. Attempting to reconnect...');
});

socket.on('reconnect', (attemptNumber) => {
    console.log('Reconnected after', attemptNumber, 'attempts');
    addSystemMessage('Reconnected to server.');
    if (username) {
        socket.emit('join', { username });
    }
});

setInterval(() => {
    socket.emit('ping', {}, (response) => {
        if (response && response.status !== 'ok') {
            console.error('Ping failed:', response.message);
        }
    });
}, 30000); 