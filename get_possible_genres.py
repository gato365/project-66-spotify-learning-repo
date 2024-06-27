import os
import requests
from dotenv import load_dotenv
import pandas as pd
# Load environment variables
load_dotenv()

def get_spotify_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, data={
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    if auth_response.status_code != 200:
        raise Exception(f"Failed to get access token: {auth_response.text}")
    return auth_response.json()['access_token']

def get_possible_genres(access_token=None):
    if access_token is None:
        access_token = get_spotify_access_token()  
    
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to get genre information: {response.text}")
    
    genre_data = response.json()
    genres = genre_data['genres']  

    df = pd.DataFrame({'genre': genres})
    return df

    genres = response.json()['genres']  
    df = pd.DataFrame(genres, columns=['genre'])  
    return df


client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
access_token = get_spotify_access_token(client_id, client_secret)
possible_genres_df_queries = get_possible_genres(access_token=access_token)
print(possible_genres_df_queries)


