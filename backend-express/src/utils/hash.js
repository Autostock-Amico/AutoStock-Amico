const { hash, verify } = require('@node-rs/argon2');

async function hashPassword(plainPassword) {
  return hash(plainPassword);
}

async function verifyPassword(plainPassword, hashedPassword) {
  try {
    return await verify(hashedPassword, plainPassword);
  } catch (error) {
    // El hash guardado no es argon2 (por ejemplo, un usuario viejo con bcrypt)
    return false;
  }
}

module.exports = { hashPassword, verifyPassword };
