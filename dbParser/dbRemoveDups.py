from pymongo import MongoClient

address = "localhost"
port = 27017


def main():
    client = MongoClient(address, port)
    db = client.random  # database
    collection = db.restaurants  # collection
    print("starts removing duplicates")
    patents = []
    count = 0
    for item in collection.find():
        if item['restaurantId'] not in patents:
            patents.append(item['restaurantId'])
        else:
            count += 1
            collection.delete_one(item)
    print("finish removing duplicates, number of removed duplicate:", count)


if __name__ == "__main__":
    main()
