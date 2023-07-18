import ast
import os
import sys
from collections import Counter
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dataProcessing import read_all_restaurant, preprocess_data
client = MongoClient(os.getenv('MONGODB_HOST', os.getenv('MONGODB_PORT')))
db = client.random  # database
restaurant_collection = db.restaurants  # collection
user_collection = db.users


# def recommend(user_likes):
uid = sys.argv[1]
user_likes = ast.literal_eval(sys.argv[2])
sys.stdout.flush()
data, pictures = read_all_restaurant()
preprocessed_all_data, all_data = preprocess_data(data, pictures)
tfidf = TfidfVectorizer()
vec = tfidf.fit(preprocessed_all_data['Tags'])
tfidf_matrix = vec.transform(preprocessed_all_data['Tags'])
user_liked_restaurants = preprocessed_all_data[preprocessed_all_data['ID'].isin(user_likes)]
user_profile = ""
# print(user_liked_restaurants)
for row, item in user_liked_restaurants.iterrows():
    user_profile += item['Tags']
user_matrix = vec.transform([user_profile])
cosine_similarities = cosine_similarity(user_matrix, tfidf_matrix)
# print(cosine_similarities)
all_data['similarity'] = cosine_similarities[0]
recommendations = all_data[~all_data['ID'].isin(user_likes)]
recommendations.sort_values(by='similarity', ascending=False, inplace=True)

keywords = user_profile.split()
counts = Counter(keywords)
keywords = sorted(counts, key=lambda x: counts[x], reverse=True)
filters = {'uid': uid}
update = {'$set': {
    'recommendations': recommendations['ID'].tolist(),
    'keywords': keywords,
}}  # Use $push to add a value to the array field
result = user_collection.update_one(filters, update)
if result.matched_count > 0:
    print('0')
else:
    print('1')
# print(recommendations.to_json(orient='records'))


# recommend(read_user_likes_raw_data('random_admin'))
