const mongoose = require('mongoose');

mongoose.connect('mongodb://127.0.0.1:27017/restaurants', {useNewURLParser: true})
        .then(()=> {
            console.log('数据库连接成功');
        })
        .catch(error => console.log('数据库连接失败'))
        