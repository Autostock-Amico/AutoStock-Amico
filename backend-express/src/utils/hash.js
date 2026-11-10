const bcrypt = require('bcryptjs');

const SALT_ROUNDS = 10;

async function hashPassword(plainPassword) {
  return bcrypt.hash(plainPassword, SALT_ROUNDS);
}

async function verifyPassword(plainPassword, hash) {
  try {
    return await bcrypt.compare(plainPassword, hash);
  } catch (error) {
    // El hash guardado no es bcrypt (por ejemplo, un usuario viejo con argon2)
    return false;
  }
}

module.exports = { hashPassword, verifyPassword };
