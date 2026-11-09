import axiosClient from '../api/axiosClient';

export const getProducts = async () => {
  const { data } = await axiosClient.get('/products/');
  return data;
};

export const getCriticalStock = async () => {
  const { data } = await axiosClient.get('/products/critical-stock');
  return data;
};

export const createProduct = async (product) => {
  const { data } = await axiosClient.post('/products/', product);
  return data;
};

export const updateProduct = async (id, product) => {
  const { data } = await axiosClient.put(`/products/${id}`, product);
  return data;
};

export const deleteProduct = async (id) => {
  await axiosClient.delete(`/products/${id}`);
};

export const adjustStock = async (id, type, quantity) => {
  const { data } = await axiosClient.patch(`/products/${id}/stock`, { type, quantity });
  return data;
};

const downloadReport = async (format, filename) => {
  const response = await axiosClient.get(`/reports/${format}`, { responseType: 'blob' });
  const url = window.URL.createObjectURL(response.data);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  window.URL.revokeObjectURL(url);
};

export const downloadExcelReport = () => downloadReport('excel', 'reporte_inventario.xlsx');
export const downloadPdfReport = () => downloadReport('pdf', 'reporte_inventario.pdf');

export const isCritical = (product) => Number(product.currentStock) <= Number(product.minStock);

export const getApiErrorMessage = (err, fallback) => {
  const data = err?.response?.data;
  if (typeof data?.detail === 'string') return data.detail;
  if (Array.isArray(data?.detail)) return data.detail.map((d) => d.msg).join('. ');
  return data?.error || data?.message || fallback;
};
