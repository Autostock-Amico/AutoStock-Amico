const jwt = require('jsonwebtoken');

function getBearerToken(header) {
  if (!header) return null;
  const [scheme, token] = header.trim().split(/\s+/);
  return scheme === 'Bearer' && token ? token : null;
}

function authenticateToken(req, res, next) {
  const token = getBearerToken(req.headers.authorization);
  if (!token) {
    return res.status(401).json({ detail: 'Token no proporcionado, inválido o expirado' });
  }

  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    return next();
  } catch (error) {
    return res.status(401).json({ detail: 'Token no proporcionado, inválido o expirado' });
  }
}

module.exports = authenticateToken;
