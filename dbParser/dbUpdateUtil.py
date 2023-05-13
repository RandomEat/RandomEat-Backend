from pymongo import MongoClient
from geopy.geocoders import Nominatim

address = "localhost"
port = 27017

geolocator = Nominatim(user_agent="random", timeout=10)


def db_update_region():
    client = MongoClient(address, port)
    db = client.random  # database
    collection = db.restaurants  # collection
    print("starts updating region")
    for item in collection.find():
        lat = item['location']['lat']
        lon = item['location']['lon']
        print(lat, lon)
        location = geolocator.reverse(f"{lat}, {lon}")
        region = location.raw['address'].get('town') if location.raw['address'].get('town') is not None \
            else location.raw['address'].get('suburb')
        update = {'$set': {'location.region': region}}
        result = collection.update_one({'_id': item['_id']}, update)
        print('Matched Documents:', result.matched_count)
        print('Modified Documents:', result.modified_count)
    print("finish updating region")


if __name__ == "__main__":
    db_update_region()
