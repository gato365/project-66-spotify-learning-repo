import os
import requests
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

def get_spotify_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    if auth_response.status_code != 200:
        raise Exception(f"Failed to get access token: {auth_response.text}")
    return auth_response.json()['access_token']

def search_spotify(queries, search_type, access_token):
    search_results = []
    for query in queries:
        search_url = 'https://api.spotify.com/v1/search'
        headers = {'Authorization': f'Bearer {access_token}'}
        params = {'q': query, 'type': search_type, 'limit': 1}  # Set limit to 1 for demo purposes
        response = requests.get(search_url, headers=headers, params=params)
        if response.status_code == 200:
            search_results.extend(response.json()[f'{search_type}s']['items'])
        else:
            print(f"Failed to search for {query}: {response.text}")
    return search_results

def get_tracks(queries=None, ids=None, access_token=None):
    if queries is not None:
        search_results = search_spotify(queries, "track", access_token=access_token)
        ids = [track['id'] for track in search_results]
    
    if not ids:
        raise ValueError("No track ids provided or found.")
    
    url = "https://api.spotify.com/v1/tracks"
    headers = {'Authorization': f'Bearer {access_token}'}
    
    if len(ids) > 1:
        params = {'ids': ','.join(ids), 'market': 'US'}
        response = requests.get(url, headers=headers, params=params)
    else:
        url += f"/{ids[0]}"
        params = {'market': 'US'}
        response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to get track info: {response.text}")
    
    result = response.json()
    
    if len(ids) > 1:
        tracks = result['tracks']
        data = {
            'track_id': [track['id'] for track in tracks],
            'track_name': [track['name'] for track in tracks],
            'popularity': [track['popularity'] for track in tracks],
            'disc_number': [track['disc_number'] for track in tracks],
            'duration_ms': [track['duration_ms'] for track in tracks],
            'explicit': [track['explicit'] for track in tracks],
            'album_type': [track['album']['album_type'] for track in tracks],
            'album_name': [track['album']['name'] for track in tracks],
            'album_release_date': [track['album']['release_date'] for track in tracks],
            'album_release_date_precision': [track['album']['release_date_precision'] for track in tracks],
            'album_total_tracks': [track['album']['total_tracks'] for track in tracks],
            'artist_id': [', '.join([artist['id'] for artist in track['artists']]) for track in tracks],
            'artist_name': [', '.join([artist['name'] for artist in track['artists']]) for track in tracks]
        }
        df = pd.DataFrame(data)
    else:
        track = result
        data = {
            'track_id': track['id'],
            'track_name': track['name'],
            'popularity': track['popularity'],
            'disc_number': track['disc_number'],
            'duration_ms': track['duration_ms'],
            'explicit': track['explicit'],
            'album_type': track['album']['album_type'],
            'album_name': track['album']['name'],
            'album_release_date': track['album']['release_date'],
            'album_release_date_precision': track['album']['release_date_precision'],
            'album_total_tracks': track['album']['total_tracks'],
            'artist_id': ', '.join([artist['id'] for artist in track['artists']]),
            'artist_name': ', '.join([artist['name'] for artist in track['artists']])
        }
        df = pd.DataFrame([data])
    
    return df

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
access_token = get_spotify_access_token(client_id, client_secret)
queries = ["Risk", "Euphoria", "Alright"]

track_df_queries = get_tracks(queries=queries, access_token=access_token)
print(track_df_queries)
