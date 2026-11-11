// Reglas del formulario de productos (sin dependencias de la vista)
export const SKU_REGEX = /^[A-Z]{3}-\d{3,}$/;
export const MAX_STOCK = 10000;

export const EMPTY_PRODUCT = {
  sku: '',
  name: '',
  category: '',
  costPrice: 0,
  salePrice: 0,
  currentStock: 0,
  minStock: 0
};

export const toProductForm = (product) => {
  if (!product) return { ...EMPTY_PRODUCT };
  return Object.fromEntries(Object.keys(EMPTY_PRODUCT).map(key => [key, product[key] ?? EMPTY_PRODUCT[key]]));
};

export const validateProduct = (data) => {
  if (!SKU_REGEX.test(data.sku)) return 'El SKU debe contener 3 letras, un guión y al menos 3 números (Ej: ART-001).';
  if (!data.name.trim() || !data.category.trim()) return 'Por favor complete todos los campos obligatorios.';
  if (data.currentStock > MAX_STOCK) return 'El stock no puede superar el límite máximo de 10.000 unidades.';
  return '';
};

export const validateStockMovement = (type, qty, current) => {
  if (!Number.isInteger(qty) || qty <= 0) return 'La cantidad debe ser un número entero mayor a 0.';
  if (type === 'OUT' && qty > current) {
    return `Stock insuficiente. Intenta retirar ${qty} u. pero solo hay ${current} u. disponibles.`;
  }
  if (type === 'IN' && current + qty > MAX_STOCK) {
    return `No se puede superar el stock máximo permitido de 10.000 unidades. (Stock actual: ${current} u.)`;
  }
  return '';
};
