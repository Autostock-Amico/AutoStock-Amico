const express = require('express');
const mongoose = require('mongoose');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
app.use(express.json());

const MONGO_URI = process.env.MONGO_URI || 'mongodb://root:example@mongo:27017/autostock?authSource=admin';

mongoose.connect(MONGO_URI)
  .then(() => console.log('MongoDB conectado exitosamente en Express'))
  .catch((err) => console.error('Error al conectar MongoDB en Express:', err));

const productRoutes = require('./routes/productRoutes');
const reportRoutes = require('./routes/reportRoutes');

app.use('/api/products', productRoutes);
app.use('/api/reports', reportRoutes);

app.get('/', (req, res) => {
  res.send('Backend Express AutoStock corriendo perfectamente');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor Express escuchando en puerto ${PORT}`);
});
