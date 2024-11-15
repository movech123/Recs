import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.decomposition import TruncatedSVD
import time
import json
import numpy as np
import cupy as cp

def recommend_shows(username, k=5):
    x = time.time()

    np.random.seed(42)
    # MongoDB connection setup
    uri = "your-db-connection-string"
    client = MongoClient(uri)
    database = client.get_database("users")
    users_collection = database.get_collection("rankings")
    # Fetch user data from MongoDB
    
    documents = list(users_collection.find())

    client.close()
    # Load anime titles from the JSON file
    with open('myapp/all_anime_output.json', 'r') as f:
        anime_data = json.load(f)
    anime_titles = [entry['node']['title'] for entry in anime_data]
    anime_ids = [entry['node']['id'] for entry in anime_data]
    
    # Create a dictionary of user ratings
    users = []

    rows = []
    anime_index = {anime: idx for idx, anime in enumerate(anime_titles)}
    for doc in documents:
        user = doc['_id']
        user_data = doc[user]

        # Initialize a row of zeros
        row = np.zeros(len(anime_titles))

        # Fill in ratings for each anime in user data
        for anime, rating in user_data.items():
            if anime in anime_index:
                row[anime_index[anime]] = rating


        users.append(user)
        rows.append(row)
        
        
    rows = np.array(rows)
    threshold = 3
    
    non_zero_counts = np.count_nonzero(rows, axis=0)


    matrix = rows[:, non_zero_counts >= threshold]
    user_index = users.index(username)
    
    missing_mask = (matrix == 0)
    
    unwatched_shows = np.where(missing_mask[user_index])[0]
    
    svd = TruncatedSVD(n_components=73)

    for i in range(4):
   
        matrix_truncated = svd.fit_transform(matrix)  # Apply SVD
    
   
        predicted_matrix = np.dot(matrix_truncated, svd.components_)

        predicted_matrix = np.clip(predicted_matrix, 0, 10)

        matrix[missing_mask] = predicted_matrix[missing_mask]
            
    
    def get_top_unwatched_shows(predicted_matrix, k=5):
        # Locate the row index for the given username

        user_predictions = predicted_matrix[user_index]
    
        # Identify unwatched shows (i.e., entries where the rating is 0)
        
        sorted_unwatched_shows = unwatched_shows[np.argsort(user_predictions[unwatched_shows])[::-1]]
        top_shows_indices = sorted_unwatched_shows[:k]
        
        top_shows = [anime_titles[int(i)] for i in top_shows_indices]
        ids = [anime_ids[int(i)] for i in top_shows_indices]
        top_ratings = user_predictions[top_shows_indices].tolist()
        return list(zip(top_shows, top_ratings, ids))

    # Get recommendations for the specified user
    top_shows = get_top_unwatched_shows(predicted_matrix, 5)
    print(time.time()-x)
    return json.dumps(top_shows)
