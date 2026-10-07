const express = require('express');
const router = express.Router();
const { getProducts, createProduct, updateProduct, deleteProduct, updateStock } = require('../controllers/productController');
const authenticateToken = require('../middlewares/authMiddleware');

router.get('/', authenticateToken, getProducts);
router.post('/', authenticateToken, createProduct);
router.put('/:id', authenticateToken, updateProduct);
router.delete('/:id', authenticateToken, deleteProduct);
router.patch('/:id/stock', authenticateToken, updateStock);

module.exports = router;
