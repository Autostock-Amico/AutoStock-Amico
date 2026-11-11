import axiosClient from '../api/axiosClient';

export const getCategories = async () => {
  const { data } = await axiosClient.get('/categories');
  return data;
};

export const createCategory = async (name) => {
  const { data } = await axiosClient.post('/categories', { name, description: '' });
  return data;
};
