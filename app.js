const express = require('express');
const app = express();
const axios = require('axios');
const {spawn} = require('child_process');
require('./models/mongo')
const Restaurant = require('./models/restaurant')
const User = require('./models/user');
const { join } = require('path');
const APPID = process.env.APPID
const SECRET = process.env.SECRET
const defaultRestaurantsID = [126, 903, 939, 1535, 1801, 5091, 5875, 6781, 8307, 8477]

app.use(express.urlencoded({
    extended: true
}))
app.use(express.json());  

// get user uid
app.get('/getUserProfile', async (req, res) => {
    let code = req.query.userCode; // userCode
    let url = "https://api.weixin.qq.com/sns/jscode2session?&appid="+APPID+"&secret="+SECRET+"&js_code="+code+"&grant_type=authorization_code"
    await axios.get(url)
    .then((response) => {
        const { openid, session_key } = response.data;
        console.log('OpenID:', openid);
        console.log('SessionKey:', session_key);
    })
    .catch((error) => {
    console.error('Error:', error);
    });
    openid = 'random_admin'
    User.findOne({ uid: openid })
    .then(async (user) => {
        if (user) {
            // if existed user, return uid, newUser=false, userLikes, recommendations
            console.log('User exists');
            let recommendations = await getRecommendation(user);
            const response = {
                uid: openid,
                newUser: false,
                userLikes: user.likes,
                recommendations: recommendations
            };
            res.status(200).send(response);
        } else {
            // if new user return uid, newUser=true, 10 restaurants for profile setup
            console.log('User does not exist');
            var defaultRestaurants = [];
            defaultRestaurantsID.forEach(async (id) => {
                let restaurant = await Restaurant.findOne({uid: id});
                defaultRestaurants.push(restaurant);
            });
            const response = {
                uid: openid,
                newUser: true,
                defaultRestaurants: defaultRestaurants
            };
            res.json(response);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
})


// post user new likes 
app.post('/postUserNewLikes', async (req, res) => {
    let uid = req.query.uid; // uid
    let newUser = req.body.newUser;// bool flag
    let newLikes = req.body.newLikes;
    console.log(uid)
    console.log(newUser)
    console.log(newLikes)
    // check flag if needs to send recommendations
    User.findOneAndUpdate(
        {uid: uid}, 
        {$push: {likes: {$each: newLikes}}}
    ).then((user) => {
        console.log('update user likes successfully');
        res.status(200).send(user.likes)
    })

    if(newUser){

    }
    // if newUser
    // return userLikes, recommendations
})


async function getRecommendation(user){
    return new Promise ((resolve, reject) => {
        const pythonProcess = spawn('python3', ['recommender/recommender.py', JSON.stringify(user.likes)]);
        let jsonData = '';
        pythonProcess.stdout.on('data', (data) => {
            // console.log("get recommendations successful")
            jsonData += data.toString()
        });

        // pythonProcess.stderr.on('data', (data) => {
        //     console.log("get recommendations unsuccessful")
        //     return data
        // });
        pythonProcess.on('close', (code) => {
            const parsedData = JSON.parse(jsonData);
            let restaurantIDs = parsedData.split(',').map(Number);
            console.log(restaurantIDs);
            resolve(restaurantIDs)
        });
    });
}


app.listen(3000, () => {
    console.log('服务器连接成功');
});
