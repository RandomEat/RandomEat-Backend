const mongoose = require('mongoose');

const diningHistorySchema = new mongoose.Schema({
    restaurantId: {type: Number, required: true },
    timestamp: {type: String, required: true }
  });

const userSchema = new mongoose.Schema({
    uid: String,
    likes: [Number],
    favorites: [Number],
    diningHistory: [diningHistorySchema],
    keywords: [String],
    recommendations: [Number],
    
})

const User = mongoose.model('User', userSchema);

module.exports = User;