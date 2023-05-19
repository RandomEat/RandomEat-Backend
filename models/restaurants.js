const mongoose = require('mongoose');

const restaurantSchema = new mongoose.Schema({
    name: String,
    location: {},
    price: String,
    category: [String]
})

const Restaurant = mongoose.model('Restaurant', restaurantSchema);

module.exports = Restaurant;