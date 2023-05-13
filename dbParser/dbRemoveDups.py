from pymongo import MongoClient

address = "localhost"
port = 27017


def main():
    client = MongoClient(address, port)
    db = client.random  # database
    collection = db.restaurants  # collection
    print("removing duplicates")
    patents = []
    count = 0
    for item in collection.find():
        if item['restaurantId'] not in patents:
            patents.append(item['restaurantId'])
        else:
            collection.delete_one(item)
    print("finish removing duplicates")

if __name__ == "__main__":
    main()
