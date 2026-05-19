document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');

    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `mb-3 ${isUser ? 'text-end' : ''}`;
        messageDiv.innerHTML = `
            <div class="d-inline-block p-3 rounded ${isUser ? 'bg-primary text-white' : 'bg-light'}">
                ${isUser ? '<i class="fas fa-user me-2"></i>' : '<i class="fas fa-robot me-2"></i>'}
                ${message}
            </div>
        `;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        addMessage(message, true);
        chatInput.value = '';

        try {
            console.log('Sending message:', message);
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            console.log('Response status:', response.status);
            console.log('Response ok:', response.ok);

            if (response.ok) {
                const data = await response.json();
                console.log('Response data:', data);
                if (data.response) {
                    addMessage(data.response);
                } else if (data.error) {
                    addMessage('Error: ' + data.error);
                } else {
                    addMessage('Received unexpected response from server');
                }
            } else {
                let errorMessage = 'Sorry, I encountered an error. Please try again.';
                try {
                    const errorData = await response.json();
                    if (errorData.error) {
                        errorMessage = 'Error: ' + errorData.error;
                    }
                } catch (e) {
                    errorMessage += ' (Status: ' + response.status + ')';
                }
                console.error('Error response:', errorMessage);
                addMessage(errorMessage);
            }
        } catch (error) {
            console.error('Fetch error:', error);
            addMessage('Sorry, I encountered an error. Please try again. Error: ' + error.message);
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });
});