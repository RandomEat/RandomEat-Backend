from pymongo import MongoClient
from geopy.geocoders import Nominatim
from dotenv import dotenv_values

env_vars = dotenv_values('.env')

geolocator = Nominatim(user_agent="random", timeout=10)
client = MongoClient(env_vars['MONGODB_HOST'], int(env_vars['MONGODB_PORT']))
db = client.random  # database
restaurant_collection = db.restaurants  # collection
user_collection = db.users


def db_update_region():
    print("starts updating region")
    for item in restaurant_collection.find():
        lat = item['location']['lat']
        lon = item['location']['lon']
        print(lat, lon)
        location = geolocator.reverse(f"{lat}, {lon}")
        region = location.raw['address'].get('town') if location.raw['address'].get('town') is not None \
            else location.raw['address'].get('suburb')
        update = {'$set': {'location.region': region}}
        result = restaurant_collection.update_one({'_id': item['_id']}, update)
        print('Matched Documents:', result.matched_count)
        print('Modified Documents:', result.modified_count)
    print("finish updating region")


def db_get_all_restaurant_id():
    all_restaurant_id = []
    for item in restaurant_collection.find():
        all_restaurant_id.append(item['restaurantId'])
    return all_restaurant_id


def db_update_user_likes(uid, new_likes):
    user = user_collection.find_one({'uid': uid})
    for like in new_likes:
        update = {'$set': {f'likes.{like}': 10}}
        user_collection.update_one({'_id': user['_id']}, update)


if __name__ == "__main__":
    db_update_user_likes('random_admin', db_get_all_restaurant_id()[:10])
