const WebSocket = require('ws');

// Funcție pentru a trimite cereri către WebSocket
function sendRequest(route, message) {
    const ws = new WebSocket(`ws://localhost:8765${route}`);

    ws.on('open', () => {
        console.log(`Connected to ${route}`);
        ws.send(message);
    });

    ws.on('message', (data) => {
        console.log(`Received response: ${data}`);
        ws.close();
    });

    ws.on('close', () => {
        console.log('Connection closed');
    });

    ws.on('error', (error) => {
        console.error(`Error: ${error.message}`);
    });
}

// Exemplu de utilizare
sendRequest('/summarize', 'hello world');
sendRequest('/po', 'sample message');



//exemplu pe car l-am putea folosi pe parte client pentru a trimite la websocket un request