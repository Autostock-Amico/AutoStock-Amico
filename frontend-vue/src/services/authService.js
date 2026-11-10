import axiosClient from '../api/axiosClient';

export const login = async (identifier, password) => {
  const { data } = await axiosClient.post('/auth/login', { identifier, password });
  localStorage.setItem('token', data.token);
  return data;
};

export const register = async ({ username, email, password }) => {
  const { data } = await axiosClient.post('/auth/register', { username, email, password });
  return data;
};

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};
