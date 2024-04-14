// const express = require('express');
// const app = express();
// const port = 3000;

// app.get('/getTime', (req, res) => {
//     const serverTime = Date.now(); // Current server time in milliseconds since the Unix epoch
//     res.json({ serverTime });
// });

// app.listen(port, () => {
//     console.log(`Server running at http://localhost:${port}`);
// });

const express = require('express');
const app = express();
const port = 3000;

app.get('/getTime', (req, res) => {
    const serverTime = Date.now(); // Server's current time in milliseconds since Unix epoch
    res.json({ serverTime });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
