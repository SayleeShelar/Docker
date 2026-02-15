const express = require('express');
const mongoose = require('mongoose');

const app = express();
app.use(express.json());

// MongoDB connection URL
// When running locally (outside Docker): use localhost:27017
// When running in Docker: use mongo:27017 (container name)
const MONGO_URL = process.env.MONGO_URL || 'mongodb://admin:password@localhost:27017/mydb?authSource=admin';

// Connect to MongoDB
mongoose.connect(MONGO_URL)
  .then(() => {
    console.log('✅ Connected to MongoDB successfully!');
    console.log('📍 MongoDB URL:', MONGO_URL);
  })
  .catch(err => {
    console.error('❌ MongoDB connection error:', err.message);
  });

// Define a simple User schema
const userSchema = new mongoose.Schema({
  name: String,
  email: String,
  createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);

// Routes
app.get('/', (req, res) => {
  res.send(`
    <h1>Node.js + MongoDB Docker Demo</h1>
    <p>✅ Server is running!</p>
    <p>📊 <a href="/users">View all users</a></p>
    <p>➕ <a href="/add-user">Add sample user</a></p>
    <p>🗄️ <a href="http://localhost:8081" target="_blank">Open Mongo Express</a> (admin/pass)</p>
  `);
});

// Get all users
app.get('/users', async (req, res) => {
  try {
    const users = await User.find();
    res.json({
      success: true,
      count: users.length,
      users: users
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// Add a sample user
app.get('/add-user', async (req, res) => {
  try {
    const user = new User({
      name: `User ${Date.now()}`,
      email: `user${Date.now()}@example.com`
    });
    await user.save();
    res.json({
      success: true,
      message: 'User added successfully!',
      user: user
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
