const express = require('express');
const router = express.Router();
const reportController = require('../controllers/reportController');

router.get('/excel', reportController.getExcelReport);
router.get('/pdf', reportController.getPDFReport);

module.exports = router;
