const express = require('express');
// Install: npm install node-fetch // Node.js 18 or newer, you do not need node-fetch
const app = express();
const PORT = 8080;
// Route to get random dog image
app.get('/random-dog', async (req, res) => {
    try {
        const response = await fetch('https://dog.ceo/api/breeds/image/random');
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        const data = await response.json();
        res.json({
            status: 'success',
            image: data.message
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/random-dog `);
})
