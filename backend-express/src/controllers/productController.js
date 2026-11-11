const mongoose = require('mongoose');
const Product = require('../models/Product');

const ENTRY_TYPES = ['ENTRY', 'ADD', 'IN'];
const EXIT_TYPES = ['EXIT', 'SUBTRACT', 'OUT'];
const EDITABLE_FIELDS = ['name', 'sku', 'category', 'costPrice', 'salePrice', 'currentStock', 'minStock'];

const sendError = (res, status, detail) => res.status(status).json({ detail });

const escapeRegex = (text) => text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

const isValidId = (id) => mongoose.Types.ObjectId.isValid(id);

const buildSearchQuery = ({ search, category }) => {
  const query = {};
  if (search && search.trim()) {
    const searchRegex = new RegExp(escapeRegex(search.trim()), 'i');
    query.$or = [{ name: searchRegex }, { sku: searchRegex }];
  }
  if (category && category.trim()) {
    query.category = category.trim();
  }
  return query;
};

const pickEditableFields = (body) => {
  const data = {};
  EDITABLE_FIELDS.forEach((field) => {
    if (body[field] !== undefined && body[field] !== null) data[field] = body[field];
  });
  if (typeof data.sku === 'string') data.sku = data.sku.trim().toUpperCase();
  if (typeof data.name === 'string') data.name = data.name.trim();
  if (typeof data.category === 'string') data.category = data.category.trim();
  return data;
};

const skuInUse = (sku, excludeId) => {
  const query = { sku };
  if (excludeId) query._id = { $ne: excludeId };
  return Product.exists(query);
};

const handleWriteError = (res, error, fallback) => {
  if (error.name === 'ValidationError') {
    const messages = Object.values(error.errors).map((e) => e.message);
    return sendError(res, 400, messages.join('. '));
  }
  if (error.code === 11000) return sendError(res, 400, 'Ya existe un producto con este SKU');
  return sendError(res, 500, fallback);
};

const getProducts = async (req, res) => {
  try {
    const products = await Product.find(buildSearchQuery(req.query)).sort({ createdAt: -1 });
    return res.status(200).json(products);
  } catch (error) {
    return sendError(res, 500, 'Error interno al obtener los productos');
  }
};

const getCriticalStock = async (req, res) => {
  try {
    const products = await Product.find({ $expr: { $lte: ['$currentStock', '$minStock'] } });
    return res.status(200).json(products);
  } catch (error) {
    return sendError(res, 500, 'Error al obtener productos con stock crítico');
  }
};

const createProduct = async (req, res) => {
  const data = pickEditableFields(req.body);
  try {
    if (data.sku && (await skuInUse(data.sku))) {
      return sendError(res, 400, 'Ya existe un producto con este SKU');
    }
    const product = await Product.create(data);
    return res.status(201).json(product);
  } catch (error) {
    return handleWriteError(res, error, 'Error interno al crear el producto');
  }
};

const updateProduct = async (req, res) => {
  const { id } = req.params;
  if (!isValidId(id)) return sendError(res, 400, 'ID de producto inválido');

  const data = pickEditableFields(req.body);
  try {
    if (data.sku && (await skuInUse(data.sku, id))) {
      return sendError(res, 400, 'Ya existe un producto con este SKU');
    }
    const product = await Product.findByIdAndUpdate(id, data, { new: true, runValidators: true });
    if (!product) return sendError(res, 404, 'Producto no encontrado');
    return res.status(200).json(product);
  } catch (error) {
    return handleWriteError(res, error, 'Error interno al actualizar el producto');
  }
};

const deleteProduct = async (req, res) => {
  const { id } = req.params;
  if (!isValidId(id)) return sendError(res, 400, 'ID de producto inválido');

  try {
    const product = await Product.findByIdAndDelete(id);
    if (!product) return sendError(res, 404, 'Producto no encontrado');
    return res.status(204).send();
  } catch (error) {
    return sendError(res, 500, 'Error interno al eliminar el producto');
  }
};

const parseMovementType = (type) => {
  const value = typeof type === 'string' ? type.toUpperCase() : '';
  if (ENTRY_TYPES.includes(value)) return 'ENTRY';
  if (EXIT_TYPES.includes(value)) return 'EXIT';
  return null;
};

const updateStock = async (req, res) => {
  const { id } = req.params;
  const { quantity } = req.body;
  const movement = parseMovementType(req.body.type);

  if (!isValidId(id)) return sendError(res, 400, 'ID de producto inválido');
  if (!Number.isInteger(quantity) || quantity <= 0) {
    return sendError(res, 400, 'La cantidad debe ser un número entero mayor a cero');
  }
  if (!movement) return sendError(res, 400, 'El tipo debe ser "IN" o "OUT"');

  const isEntry = movement === 'ENTRY';
  const query = isEntry ? { _id: id } : { _id: id, currentStock: { $gte: quantity } };

  try {
    const updated = await Product.findOneAndUpdate(
      query,
      { $inc: { currentStock: isEntry ? quantity : -quantity } },
      { new: true }
    );
    if (updated) return res.status(200).json(updated);

    const exists = await Product.exists({ _id: id });
    return exists
      ? sendError(res, 400, 'Stock insuficiente para realizar la operación')
      : sendError(res, 404, 'Producto no encontrado');
  } catch (error) {
    return sendError(res, 500, 'Error interno al actualizar el stock');
  }
};

module.exports = {
  getProducts,
  createProduct,
  updateProduct,
  deleteProduct,
  updateStock,
  getCriticalStock,
};
