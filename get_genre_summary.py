import os
import requests
from dotenv import load_dotenv
import pandas as pd
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
def get_genre_summary(genre, access_token=None):
    if access_token is None:
        access_token = get_spotify_access_token() 

    tracks_df = get_genre_tracks(genre, access_token=access_token)
    track_ids = tracks_df['track_id'].tolist()

    features_df = get_track_audio_features(track_ids, access_token=access_token)

    features_to_summarize = ['danceability', 'energy', 'loudness', 'speechiness',
                             'acousticness', 'instrumentalness', 'liveness', 'valence', 
                             'tempo', 'duration_ms', 'mode']

    summary_stats = features_df[features_to_summarize].agg(['mean', 'std']).transpose()
    summary_stats.reset_index(inplace=True)
    summary_stats.rename(columns={'index': 'feature'}, inplace=True)

    summary_stats['genre'] = genre

    return summary_stats


    genre_summary_df = get_genre_summary('jazz', access_token=access_token)
    print(genre_summary_df)