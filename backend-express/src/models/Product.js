const mongoose = require('mongoose');

const productSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'El nombre es obligatorio'],
      trim: true,
    },
    sku: {
      type: String,
      required: [true, 'El SKU es obligatorio'],
      unique: true,
      trim: true,
    },
    category: {
      type: String,
      required: [true, 'La categoría es obligatoria'],
      trim: true,
    },
    costPrice: {
      type: Number,
      required: [true, 'El precio de costo es obligatorio'],
      min: [0, 'El precio de costo no puede ser negativo'],
    },
    salePrice: {
      type: Number,
      required: [true, 'El precio de venta es obligatorio'],
      min: [0, 'El precio de venta no puede ser negativo'],
    },
    currentStock: {
      type: Number,
      default: 0,
      min: [0, 'El stock actual no puede ser negativo'],
    },
    minStock: {
      type: Number,
      default: 0,
      min: [0, 'El stock mínimo no puede ser negativo'],
    },
  },
  {
    timestamps: true,
  }
);

productSchema.set('toJSON', {
  transform: (doc, ret) => {
    ret.id = ret._id.toString();
    delete ret._id;
    delete ret.__v;
    return ret;
  },
});

module.exports = mongoose.model('Product', productSchema);
