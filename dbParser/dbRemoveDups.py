from pymongo import MongoClient
from dotenv import dotenv_values

env_vars = dotenv_values('.env')


def main():
    client = MongoClient(env_vars['MONGODB_HOST'], int(env_vars['MONGODB_PORT']))
    db = client.random  # database
    collection = db.restaurants  # collection
    print("starts removing duplicates")
    patents = []
    count = 0
    i = 1
    for item in collection.find():
        print("checking file", i)
        i += 1
        if item['restaurantId'] not in patents:
            patents.append(item['restaurantId'])
        else:
            count += 1
            collection.delete_one(item)
    print("finish removing duplicates, number of removed duplicate:", count)


if __name__ == "__main__":
    main()
