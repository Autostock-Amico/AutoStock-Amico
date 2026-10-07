const express = require('express');
const router = express.Router();
const { createProduct, updateProduct, deleteProduct } = require('../controllers/productController');
const authenticateToken = require('../middlewares/authMiddleware');

router.post('/', authenticateToken, createProduct);
router.put('/:id', authenticateToken, updateProduct);
router.delete('/:id', authenticateToken, deleteProduct);

module.exports = router;
