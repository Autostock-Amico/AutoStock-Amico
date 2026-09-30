const jwt = require('jsonwebtoken');
const User = require('../models/User');
const { hashPassword, verifyPassword } = require('../utils/hash');

async function register(req, res) {
  try {
    const { username, email, password } = req.body;

    if (!username || !email || !password) {
      return res.status(400).json({ error: 'Todos los campos son obligatorios' });
    }

    const existingUser = await User.findOne({ $or: [{ email }, { username }] });
    if (existingUser) {
      return res.status(400).json({ error: 'El usuario o email ya existe' });
    }

    const hashedPassword = await hashPassword(password);
    const newUser = new User({
      username,
      email,
      password: hashedPassword
    });

    await newUser.save();
    res.status(201).json({ message: 'Usuario registrado correctamente' });
  } catch (error) {
    res.status(500).json({ error: 'Error interno del servidor' });
  }
}

async function login(req, res) {
  try {
    const { loginIdentifier, password } = req.body;

    if (!loginIdentifier || !password) {
      return res.status(400).json({ error: 'Identificador y contraseña requeridos' });
    }

    const user = await User.findOne({
      $or: [{ email: loginIdentifier }, { username: loginIdentifier }]
    });

    if (!user) {
      return res.status(400).json({ error: 'Credenciales inválidas' });
    }

    const isValid = await verifyPassword(password, user.password);
    if (!isValid) {
      return res.status(400).json({ error: 'Credenciales inválidas' });
    }

    const token = jwt.sign(
      { id: user._id, username: user.username },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRES_IN || '8h' }
    );

    res.json({ token, user: { id: user._id, username: user.username, email: user.email } });
  } catch (error) {
    console.error('Error en login:', error);
    res.status(500).json({ error: 'Error interno del servidor' });
  }
}

async function getProfile(req, res) {
  try {
    const user = await User.findById(req.user.id).select('-password');
    if (!user) {
      return res.status(404).json({ error: 'Usuario no encontrado' });
    }
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: 'Error interno del servidor' });
  }
}

module.exports = {
  register,
  login,
  getProfile
};
