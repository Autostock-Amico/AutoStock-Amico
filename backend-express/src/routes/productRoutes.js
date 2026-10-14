const express = require('express');
const router = express.Router();
const {
  getProducts,
  createProduct,
  updateProduct,
  deleteProduct,
  updateStock,
  getCriticalStock
} = require('../controllers/productController');
const authenticateToken = require('../middlewares/authMiddleware');

// 1. Ruta de Stock Crítico (Debe ir ANTES de cualquier ruta con :id)
router.get('/critical-stock', authenticateToken, getCriticalStock);

// 2. Rutas CRUD generales
router.get('/', authenticateToken, getProducts);
router.post('/', authenticateToken, createProduct);

// 3. Rutas con parámetros :id
router.put('/:id', authenticateToken, updateProduct);
router.delete('/:id', authenticateToken, deleteProduct);
router.patch('/:id/stock', authenticateToken, updateStock);

module.exports = router;
