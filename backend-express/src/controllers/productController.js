const Product = require('../models/Product');

const createProduct = async (req, res) => {
  try {
    const { name, sku, category, costPrice, salePrice, currentStock, minStock } = req.body;

    if (!name || !sku || !category || costPrice === undefined || salePrice === undefined) {
      return res.status(400).json({ error: 'Faltan campos obligatorios' });
    }

    const skuClean = sku.trim();
    const existingSku = await Product.findOne({ sku: skuClean });
    if (existingSku) {
      return res.status(400).json({ error: 'Ya existe un producto con este SKU' });
    }

    const product = new Product({
      name: name.trim(),
      sku: skuClean,
      category: category.trim(),
      costPrice,
      salePrice,
      currentStock: currentStock ?? 0,
      minStock: minStock ?? 0,
    });

    await product.save();
    return res.status(201).json(product);
  } catch (error) {
    return res.status(500).json({ error: 'Error interno al crear el producto' });
  }
};

const updateProduct = async (req, res) => {
  try {
    const { id } = req.params;
    const { name, sku, category, costPrice, salePrice, currentStock, minStock } = req.body;

    const product = await Product.findById(id);
    if (!product) {
      return res.status(404).json({ error: 'Producto no encontrado' });
    }

    if (sku && sku.trim() !== product.sku) {
      const skuClean = sku.trim();
      const duplicate = await Product.findOne({ sku: skuClean, _id: { $ne: id } });
      if (duplicate) {
        return res.status(400).json({ error: 'El nuevo SKU ya esta registrado en otro producto' });
      }
      product.sku = skuClean;
    }

    if (name) product.name = name.trim();
    if (category) product.category = category.trim();
    if (costPrice !== undefined) product.costPrice = costPrice;
    if (salePrice !== undefined) product.salePrice = salePrice;
    if (currentStock !== undefined) product.currentStock = currentStock;
    if (minStock !== undefined) product.minStock = minStock;

    await product.save();
    return res.status(200).json(product);
  } catch (error) {
    return res.status(500).json({ error: 'Error interno al actualizar el producto' });
  }
};

const deleteProduct = async (req, res) => {
  try {
    const { id } = req.params;
    const product = await Product.findByIdAndDelete(id);

    if (!product) {
      return res.status(404).json({ error: 'Producto no encontrado' });
    }

    return res.status(200).json({ message: 'Producto eliminado exitosamente', id });
  } catch (error) {
    return res.status(500).json({ error: 'Error interno al eliminar el producto' });
  }
};

module.exports = {
  createProduct,
  updateProduct,
  deleteProduct,
};
