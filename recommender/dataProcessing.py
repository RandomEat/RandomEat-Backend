import numpy as np
from pymongo import MongoClient
from dotenv import dotenv_values
import pandas as pd
from sklearn.metrics.pairwise import haversine_distances
import jieba
import jieba.analyse
from math import radians

env_vars = dotenv_values('../dbParser/.env')
client = MongoClient(env_vars['MONGODB_HOST'], int(env_vars['MONGODB_PORT']))
db = client.random  # database
restaurant_collection = db.restaurants  # collection
user_collection = db.users
all_categories = [['烧烤烤鱼'], ['川湘麻辣'], ['卤味鸭脖'], ['台式简餐'], ['地方菜系'], ['奶茶饮品'], ['家常炒菜'],
                  ['小吃快餐'],
                  ['早点铺'], ['汉堡炸鸡'], ['港式茶餐厅'], ['粤菜早茶'], ['韩式料理'], ['香锅干锅'], ['麻辣烫冒菜']]

user_location = (radians(34.0488), radians(-118.2518))


def read_all_restaurant():
    all_restaurant_id = []
    for item in restaurant_collection.find():
        all_restaurant_id.append(item['restaurantId'])

    # fetching testing data
    raw_data = []
    for restaurant_ID in all_restaurant_id:
        restaurant = restaurant_collection.find_one(
            {'restaurantId': int(restaurant_ID)},
            {
                '_id': 0,
                'restaurantPhoto': 0,
                'location.region': 0
            })
        # restaurant['location'] =
        raw_data.append(restaurant)
    data = []
    for res in raw_data:
        data.append([res['restaurantId'],
                     res['restaurantName'],
                     list(set(res['category'])),
                     res.get('price', 20),
                     res['rate'],
                     res['location']['lat'],
                     res['location']['lon']])
    return data


def read_user_likes_raw_data(uid):
    # fetching user profile for current user
    user = user_collection.find_one({'uid': uid})
    user_likes = user['likes']
    # fetching user's likes
    user_likes = [int(i) for i in user_likes]
    return user_likes


def price_mapping(price):
    price = int(price)
    if price < 20:
        return 'low-price'
    elif price < 30:
        return 'low-mid-price'
    elif price < 50:
        return 'mid-price'
    elif price < 70:
        return 'high-mid-price'
    elif price < 100:
        return 'high-price'
    else:
        return 'fine-dining'


def preprocess_data(raw_data):
    df = pd.DataFrame(raw_data, columns=['ID', 'Name', 'Category', 'Price', 'Rate', 'lat', 'lon'])
    df['Price'] = df['Price'].apply(price_mapping)
    df['Category'] = df['Category'].str.join(',')
    # df['Distance'] = df.apply(lambda row: haversine_distances(
    #     [user_location, (radians(row['lat']), radians(row['lon']))]
    # )[0][1] * 6371, axis=1)
    df = df.drop('lat', axis=1)
    df = df.drop('lon', axis=1)

    def process_sentences(text):
        tags = jieba.analyse.extract_tags(text, topK=10)
        return ' '.join(tags)

    df['Tags'] = df['Name'].apply(process_sentences) + ' ' + df['Category'].apply(process_sentences) + ' ' + df['Price'].apply(process_sentences)
    df['Tags'] = df['Tags'].str.lower()
    df = df.drop('Name', axis=1)
    df = df.drop('Category', axis=1)
    # print(df.to_string())
    return df
