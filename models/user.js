const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    uid: String,
    likes: [Number]
})

const User = mongoose.model('User', userSchema);

module.exports = User;