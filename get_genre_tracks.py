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

def get_genre_tracks(genre, limit=20, offset=0, access_token=None):
    """Fetches tracks from a specified genre using Spotify's API."""
    if access_token is None:
        access_token = get_spotify_access_token()  # Assume this function is defined elsewhere

    url = "https://api.spotify.com/v1/search"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'q': f'genre:"{genre}"',
        'type': 'track',
        'market': 'US',
        'limit': limit,
        'offset': offset
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch tracks: {response.text}")
    
    tracks = response.json()['tracks']['items']
    
    data = []
    for track in tracks:
        if track['artists']:  
            artist_ids = ', '.join([artist['id'] for artist in track['artists']])
            artist_names = ', '.join([artist['name'] for artist in track['artists']])
        else:
            artist_ids, artist_names = None, None
        
        data.append({
            'track_id': track['id'],
            'track_name': track['name'],
            'album_type': track['album']['album_type'] if 'album' in track else None,
            'artist_id': artist_ids,
            'artist_name': artist_names
        })
    df = pd.DataFrame(data)
    return df

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
access_token = get_spotify_access_token(client_id, client_secret)
genre_tracks_df = get_genre_tracks("Country", limit = 20, offset = 20, access_token=access_token)
print(genre_tracks_df)