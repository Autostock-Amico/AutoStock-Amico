const Category = require('../models/Category');

const getCategories = async (req, res) => {
  try {
    const categories = await Category.find().sort({ createdAt: -1 });
    return res.status(200).json(categories);
  } catch (error) {
    return res.status(500).json({ error: 'Error al obtener las categorías' });
  }
};

const createCategory = async (req, res) => {
  try {
    const { name, description } = req.body;

    if (!name || !name.trim()) {
      return res.status(400).json({ error: 'El nombre de la categoría es obligatorio' });
    }

    const existingCategory = await Category.findOne({ name: name.trim() });
    if (existingCategory) {
      return res.status(400).json({ error: 'Ya existe una categoría con ese nombre' });
    }

    const category = new Category({
      name: name.trim(),
      description: description ? description.trim() : '',
    });

    await category.save();
    return res.status(201).json(category);
  } catch (error) {
    return res.status(500).json({ error: 'Error interno al crear la categoría' });
  }
};

module.exports = {
  getCategories,
  createCategory,
};
