<<<<<<< HEAD
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


# Function to get the access token
def get_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

# Function to make the API request
def get_artist_info(artist_id, access_token):
    base_url = "https://api.spotify.com/v1/artists/"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f"{base_url}{artist_id}", headers=headers)
    return response.json()

# Example usage
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')


access_token = get_access_token(client_id, client_secret)

# Example artist ID for testing
artist_id = '1uNFoZAHBGtllmzznpCI3s'  # This is the artist ID for Justin Bieber, replace with 'TI' or actual artist ID

artist_info = get_artist_info(artist_id, access_token)
print(artist_info)




=======
>>>>>>> 0b45e8c341500c333cc00d3b7f15689720691b6c

