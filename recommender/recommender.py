import ast
import json
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dataProcessing import read_all_restaurant, preprocess_data
from dataProcessing import read_user_likes_raw_data


# def recommend(user_likes):
user_likes = ast.literal_eval(sys.argv[1])
sys.stdout.flush()
all_data = preprocess_data(read_all_restaurant())
tfidf = TfidfVectorizer()
vec = tfidf.fit(all_data['Tags'])
tfidf_matrix = vec.transform(all_data['Tags'])
user_liked_restaurants = all_data[all_data['ID'].isin(user_likes)]
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
# for index, row in recommendations.iterrows():
#     print(json.dumps(row.to_dict()))
#     sys.stdout.flush()
print(json.dumps(recommendations['ID'].to_json(orient='records')[1:-1].replace('},{', '} {')))


# recommend(read_user_likes_raw_data('random_admin'))
