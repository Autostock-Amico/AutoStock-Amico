const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGO_URI || 'mongodb://santi:santi123@localhost:27017/autostock?authSource=admin');
    return conn;
  } catch (error) {
    process.exit(1);
  }
};

module.exports = connectDB;
