const express = require('express');
const app = express();

require('./models/mongo')
const Restaurant = require('./models/restaurants')

app.get('/get', async (req, res) => {
    let region = req.query.region;
    const regionList = [];
    if (region === 'random') {
        let selectedRestaurants = await Restaurant.find()
        let randomIndex = Math.floor(Math.random()*selectedRestaurants.length)
        let randomRestaurant = selectedRestaurants[randomIndex]
        res.send(randomRestaurant)
    }
    else {
        region = region.split(',')
        region.forEach(location => {
            regionList.push(location)
        })

        let selectedRestaurants = await Restaurant.find({location: {$in: regionList}})
        let randomIndex = Math.floor(Math.random()*selectedRestaurants.length)
        let randomRestaurant = selectedRestaurants[randomIndex]
        res.send(randomRestaurant)
    }
    //把字符串以逗号分隔为数组
    
})

app.listen(3000, () => {
    console.log('服务器连接成功');
});
