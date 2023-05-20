import boto3
import requests
from pymongo import MongoClient
from dotenv import dotenv_values

env_vars = dotenv_values('.env')


def upload_file_to_s3(image_url, bucket_name, object_name):
    s3 = boto3.client('s3')
    file_path = requests.get(image_url)
    try:
        s3.put_object(Body=file_path.content,
                      Bucket=bucket_name,
                      Key=object_name,
                      ACL='public-read',
                      ContentType='image/jpeg',
                      ContentDisposition='inline')
        print("File uploaded successfully.")
    except Exception as e:
        print(f"Error uploading file: {str(e)}")


def store_link_in_mongodb(bucket_name, object_name, restaurant_id):

    # Store link in MongoDB
    client = MongoClient(env_vars['MONGODB_HOST'], env_vars['MONGODB_PORT'])
    db = client.random  # database
    collection = db.restaurants  # collection
    link = f'https://{bucket_name}.s3.us-west-1.amazonaws.com/{object_name}'
    collection.update_one({"restaurantId": restaurant_id}, {'$set': {'restaurantPhoto': link}})

    print("Link stored in MongoDB.")


def get_restaurant_photo_url(bucket_name, image_url, restaurant_id):
    object_name = f"restaurantPhotos/{restaurant_id}.jpg"
    upload_file_to_s3(image_url, bucket_name, object_name)
    return f'https://{bucket_name}.s3.us-west-1.amazonaws.com/{object_name}'