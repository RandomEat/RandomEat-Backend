const express = require('express');
const app = express();
const axios = require('axios');
const {spawn} = require('child_process');
require('./models/mongo')
const Restaurant = require('./models/restaurant')
const User = require('./models/user');
const { join } = require('path');
require('dotenv').config();
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
    console.log(url)
    await axios.get(url)
    .then((response) => {
        const { openid, session_key } = response.data;
        if(openid === undefined){
            res.status(404).send({
                error: "invalid js_code"
            });
            return
        }
        console.log('OpenID:', openid);
        console.log('SessionKey:', session_key);
        //const openid = 'random_admin' // Testing
        User.findOne({ uid: openid})
        .then(async (user) => {
            if (user) {
                // if existed user, return uid, newUser=false, userLikes, recommendations
                console.log('User exists');
                let recommendations = await getRestaurants(user.recommendations);
                let userLikes = await getRestaurants(user.likes);
                const response = {
                    uid: openid,
                    newUser: false,
                    userLikes: userLikes,
                    recommendations: recommendations
                };
                res.status(200).send(response);
            } else {
                // if new user return uid, newUser=true, 10 restaurants for profile setup
                console.log('User does not exist');
                User.create({uid: openid});
                var defaultRestaurants = await getRestaurants(defaultRestaurantsID);
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
    .catch((error) => {
        console.error('Error:', error);
    });
})

// delete user
app.post('/deleteUser', async (req, res) => {
    const uid = req.query.uid;
    console.log(uid)
    await User.findOneAndDelete({uid: uid})
    .then((user) => {
        res.status(200).send({
            success: true
        })
    })
});


// post user new likes 
app.post('/postUserNewLikes', async (req, res) => {
    let uid = req.query.uid; // uid
    let newLikes = req.body.newLikes;
    console.log(uid)
    console.log(newLikes)
    // check flag if needs to send recommendations
    User.findOneAndUpdate(
        {uid: uid}, 
        {$push: {likes: {$each: newLikes}}},
        {new: true}
    ).then(async (user) => {
        console.log('update user likes successfully');
        generateRecommendation(user)
        .then((err)=>{
            if(err){
                res.status(404).send();
            }
            else{
                const response = {
                    uid: uid,
                    userLikes: user.likes,
                };
                res.status(200).send(response);
            }
        })
    })
})

function findResById(id) {
    return new Promise((resolve, reject) => {
        Restaurant.findOne({restaurantId: id})
        .then((res) => {
            resolve(res);
        });
    });
}

async function getRestaurants(restaurantIds){
    const promises = restaurantIds.map((id) => findResById(id));
    const restaurants = await Promise.all(promises);
    return restaurants;
}

async function generateRecommendation(user){
    return new Promise ((resolve, reject) => {
        // console.log(user.likes);
        const pythonProcess = spawn('python3', ['recommender/recommender.py', user.uid, JSON.stringify(user.likes)]);
        // let err = '';
        pythonProcess.stdout.on('data', (data) => {
            // console.log("get recommendations successful")
            console.log(Number(data.toString()));
            resolve(Number(data.toString()))
        });

        // pythonProcess.stderr.on('data', (data) => {
        //     console.log("get recommendations unsuccessful")
        //     console.log(data)
        // });
        // pythonProcess.on('close', (code) => {
        //     // console.log(jsonData);
        //     // const parsedData = JSON.parse(jsonData);
        //     // // console.log(parsedData);
        //     // resolve(parsedData)
        // });
    });
}


app.listen(3000, () => {
    console.log('服务器连接成功');
});
