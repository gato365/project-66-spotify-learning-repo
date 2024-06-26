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

def search_spotify(queries, access_token):
    search_results = []
    for query in queries:
        search_url = 'https://api.spotify.com/v1/search'
        headers = {'Authorization': f'Bearer {access_token}'}
        params = {'q': query, 'type': 'album', 'limit': 1}  # Set limit to 1 for demo purposes
        response = requests.get(search_url, headers=headers, params=params)
        if response.status_code == 200:
            search_results.extend(response.json()['albums']['items'])
        else:
            print(f"Failed to search for {query}: {response.text}")
    return search_results

def get_albums(queries=None, ids=None, access_token=None):
     if queries is not None:
        search_results = search_spotify(queries, access_token)
        ids = [album['id'] for album in search_results]
     if not ids:
        raise ValueError("No album ids provided or found.")
     
     url = 'https://api.spotify.com/v1/albums'
     headers = {'Authorization': f'Bearer {access_token}'}
     if len(ids) > 1:
        url += '?ids=' + ','.join(ids) + '&market=US'
        response = requests.get(url, headers=headers)
     else:
        url += '/' + ids[0] + '?market=US'
        response = requests.get(url, headers=headers)
     if response.status_code != 200:
        raise Exception(f"Failed to get album info: {response.text}")
     album_data = response.json()
     if len(ids) > 1:
        albums = album_data['albums']
     else:
        albums = [album_data]  # Make single dict a list for uniform handling

     data = []
     for album in albums:
        for artist in album['artists']:
            data.append({
                'album_id': album['id'],
                'label': album['label'],
                'album_name': album['name'],
                'artist_id': artist['id'],
                'artist_name': artist['name'],
                'release_date': album['release_date'],
                'total_tracks': album['total_tracks'],
                'album_type': album['album_type'],
                'popularity': album.get('popularity', None)  # Not all responses might have popularity
            })
     df = pd.DataFrame(data)
     return df


client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
access_token = get_spotify_access_token(client_id, client_secret)
queries = ["Red", "The Secret of Us", "SOS"]

album_df_queries = get_albums(queries=queries, access_token=access_token)
print(album_df_queries)