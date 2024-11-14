# views.py
import requests
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from myapp.auth import get_access_token
from myapp.parse import recommend_shows
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB setup
uri = "mongodb+srv://vmodalla:1234@cluster0.znmzl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
database = client.get_database("users")
users_collection = database.get_collection("rankings")
user_collection1 = database.get_collection("users")

# MyAnimeList API headers
access_token = get_access_token()
header = {
    "Authorization": f"Bearer {access_token}"
}

def index(request):
    return render(request, 'index.html')

def get_rankings(api_url, user):
    """Fetch rankings for a user if not already in the database."""
    
    api_url = f'{api_url}/{user}/animelist?fields=list_status&sort=list_score&limit=100'
    all_shows = {}
    while api_url:
       
        response = requests.get(api_url, headers=header)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'data' in data:
                shows = {d['node']['title']: d['list_status']['score'] for d in data['data']}
                all_shows.update(shows)
                
                # Check for the next page URL in the response, if it exists
                api_url = data.get('paging', {}).get('next')
            else:
                print("Unexpected data format")
                return False
            
        else:
            print(f"Failed to retrieve data for {user}, status code: {response.status_code}")
            return False
    if all_shows:
        # Update the user's ranking data in `users_collection`
        users_collection.update_one(
            {'_id': user},               # Find document by `user`
            {'$set': {user: all_shows}},   # Update with new `all_shows` data
            upsert=True                    # Insert if not found
        )

        # Ensure the user record exists in `user_collection1`
        user_collection1.update_one(
            {'name': user},                # Find document by `name`
            {'$set': {'name': user}},      # Update or insert with `name`
            upsert=True
        )
        
        print(f"Data for {user} successfully added or updated in the database.")
        return True
    
    return False
@csrf_exempt  # Temporarily disable CSRF validation for simplicity (you should add proper CSRF protection later)
def submit_rating(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        anime = data.get('anime')
        rating = data.get('rating')

        # Here you would save the rating to your database
        # For example:
        # user = User.objects.get(username=username)
        # anime_instance = Anime.objects.get(title=anime)
        # Rating.objects.create(user=user, anime=anime_instance, rating=rating)

        return JsonResponse({'status': 'success', 'message': 'Rating submitted successfully!'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
@csrf_exempt
def get_recommendations(request):
    if request.method == 'POST':
        # Parse the incoming request data
        data = json.loads(request.body)
        username = data.get('username')
        
        if username:
            # Fetch or update rankings from MyAnimeList API
            user_exists = get_rankings('https://api.myanimelist.net/v2/users', username)
            if user_exists:
                recommendations = recommend_shows(username, 73)  # Generate recommendations
                print(recommendations)
                return JsonResponse({'message': recommendations})
            else:
                return JsonResponse({'message': 'User not found'}, status=404)
        else:
            return JsonResponse({'message': 'Username is required'}, status=400)
    return JsonResponse({'message': 'Invalid method'}, status=405)
