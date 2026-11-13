require('dotenv').config();
const app = require('./src/index');

const PORT = process.env.PORT || 4000;

app.listen(PORT);