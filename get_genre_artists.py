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

def get_genre_artists(genre, limit=20, offset=0, access_token=None):
    """Fetches artists from a specified genre using Spotify's API."""
    if access_token is None:
        access_token = get_spotify_access_token()  # Assume this function is defined elsewhere

    url = "https://api.spotify.com/v1/search"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'q': f'genre:"{genre}"',
        'type': 'artist',
        'market': 'US',
        'limit': limit,
        'offset': offset
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch artists: {response.text}")
    
    artists = response.json()['artists']['items']
    
    # Prepare the data for DataFrame creation
    data = []
    for artist in artists:
        data.append({
            'artist_id': artist['id'],
            'artist_name': artist['name'],
            'followers_total': artist['followers']['total'],
            'popularity': artist['popularity'],  # Additional field for better insights
            'genres': ', '.join(artist['genres'])  # Convert list of genres to string
        })

    df = pd.DataFrame(data)
    return df

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
access_token = get_spotify_access_token(client_id, client_secret)
genre_artists_df = get_genre_artists("Country", limit = 20, offset = 20, access_token=access_token)
print(genre_artists_df)