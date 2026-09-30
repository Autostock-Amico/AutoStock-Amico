const User = require('../models/User');
const { hashPassword, verifyPassword } = require('../utils/hash');

async function register(req, res) {
  try {
    const { username, email, password } = req.body;

    if (!username || !email || !password) {
      return res.status(400).json({ error: 'Todos los campos (username, email, password) son obligatorios' });
    }

    const existente = await User.findOne({ $or: [{ username }, { email }] });
    if (existente) {
      return res.status(400).json({ error: 'El username o email ya esta en uso' });
    }

    const passwordHasheada = await hashPassword(password);
    const nuevoUsuario = new User({
      username,
      email,
      password: passwordHasheada,
    });

    await nuevoUsuario.save();
    return res.status(201).json(nuevoUsuario);
  } catch (error) {
    if (error.code === 11000) {
      return res.status(400).json({ error: 'El username o email ya esta en uso' });
    }
    if (error.name === 'ValidationError') {
      return res.status(400).json({ error: error.message });
    }
    return res.status(500).json({ error: 'Error interno del servidor' });
  }
}

async function login(req, res) {
  try {
    const { loginIdentifier, password } = req.body;

    if (!loginIdentifier || !password) {
      return res.status(400).json({ error: 'El identificador (username/email) y la contraseña son obligatorios' });
    }

    const usuario = await User.findOne({
      $or: [{ username: loginIdentifier }, { email: loginIdentifier }]
    });

    if (!usuario) {
      return res.status(401).json({ error: 'Credenciales invalidas' });
    }

    // Corregido: primero texto plano (password), segundo hash (usuario.password)
    const esPasswordValida = await verifyPassword(password, usuario.password);
    if (!esPasswordValida) {
      return res.status(401).json({ error: 'Credenciales invalidas' });
    }

    const { password: _, ...datosUsuario } = usuario.toObject();
    return res.status(200).json({
      mensaje: 'Login exitoso',
      usuario: datosUsuario
    });

  } catch (error) {
    console.error('Error en login:', error);
    return res.status(500).json({ error: 'Error interno del servidor' });
  }
}

module.exports = { register, login };
