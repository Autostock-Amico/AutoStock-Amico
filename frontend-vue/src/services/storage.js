const STORAGE_KEY = 'autostock_products_cache';

const INITIAL_MOCK_PRODUCTS = [
  { id: '1', _id: '1', sku: 'FLT-001', name: 'Filtro de Aceite', category: 'Filtros', price: 4500, stock: 12 },
  { id: '2', _id: '2', sku: 'FLT-002', name: 'Filtro de Aire', category: 'Filtros', price: 6200, stock: 3 },
  { id: '3', _id: '3', sku: 'ACE-010', name: 'Aceite Sintético 5W30', category: 'Lubricantes', price: 28500, stock: 8 },
  { id: '4', _id: '4', sku: 'PST-005', name: 'Pastillas de Freno Delanteras', category: 'Frenos', price: 18900, stock: 2 }
];

export const getLocalProducts = () => {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (!saved) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(INITIAL_MOCK_PRODUCTS));
    return INITIAL_MOCK_PRODUCTS;
  }
  try {
    return JSON.parse(saved);
  } catch (e) {
    return INITIAL_MOCK_PRODUCTS;
  }
};

export const saveLocalProducts = (products) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(products));
};
