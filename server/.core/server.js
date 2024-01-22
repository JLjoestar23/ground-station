const http = require('http');

const server = http.createServer((req, res) => {
    // Set the response header
    res.writeHead(200, {'Content-Type': 'text/plain'});

    // Send the response
    res.end('Hello, World!\n');
});

const port = 3000;

// Start the server
server.listen(port, () => {
    console.log(`Server is listening on port ${port}`);
});