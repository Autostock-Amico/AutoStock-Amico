const jwt = require('jsonwebtoken');
const User = require('../models/User');
const { hashPassword, verifyPassword } = require('../utils/hash');

const JWT_SECRET = process.env.JWT_SECRET || 'tu_clave_secreta_super_segura';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '8h';

const DUPLICATE_USER = 'El username o email ya está en uso';
const INVALID_CREDENTIALS = 'Credenciales inválidas';
const EMAIL_REGEX = /^\S+@\S+\.\S+$/;

const findByUsernameOrEmail = (username, email) =>
  User.findOne({ $or: [{ username }, { email }] });

const createToken = (user) =>
  jwt.sign(
    { sub: user._id.toString(), username: user.username, email: user.email },
    JWT_SECRET,
    { expiresIn: JWT_EXPIRES_IN }
  );

const validateRegister = ({ username, email, password }) => {
  if (!username || !username.trim()) return 'El username es obligatorio';
  if (!email || !EMAIL_REGEX.test(email)) return 'El formato del email no es válido';
  if (!password) return 'La password es obligatoria';
  return '';
};

const register = async (req, res) => {
  const validationError = validateRegister(req.body);
  if (validationError) {
    return res.status(400).json({ detail: validationError });
  }

  const username = req.body.username.trim();
  const email = req.body.email.trim().toLowerCase();

  try {
    if (await findByUsernameOrEmail(username, email)) {
      return res.status(400).json({ detail: DUPLICATE_USER });
    }
    const password = await hashPassword(req.body.password);
    const user = await User.create({ username, email, password });
    return res.status(201).json(user);
  } catch (error) {
    if (error.code === 11000) {
      return res.status(400).json({ detail: DUPLICATE_USER });
    }
    return res.status(500).json({ detail: 'Error interno al registrar el usuario' });
  }
};

const login = async (req, res) => {
  const { identifier, username, email, loginIdentifier, password } = req.body;
  const loginKey = identifier || email || username || loginIdentifier;

  if (!loginKey || !password) {
    return res.status(400).json({ detail: 'Se requiere un identificador (email o username) y contraseña' });
  }

  try {
    const user = await findByUsernameOrEmail(loginKey, loginKey.toLowerCase());
    const isValid = user && (await verifyPassword(password, user.password));
    if (!isValid) {
      return res.status(401).json({ detail: INVALID_CREDENTIALS });
    }
    return res.status(200).json({ token: createToken(user) });
  } catch (error) {
    return res.status(500).json({ detail: 'Error interno del servidor en login' });
  }
};

const getMe = (req, res) => res.status(200).json(req.user);

module.exports = { register, login, getMe };
