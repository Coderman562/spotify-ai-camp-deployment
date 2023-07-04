import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests
import base64

client_id = 'f74d125a75774bb886fea891b2324a1a'
client_secret = '4f5e9dc1a61e442bb5f6d3aa83b4d185'


class spotify:

  def __init__(self, client_id, client_secret):
    self.client_id = client_id
    self.client_secret = client_secret
    self.client_credentials_manager = SpotifyClientCredentials(
      client_id=client_id, client_secret=client_secret)
    self.sp = spotipy.Spotify(
      client_credentials_manager=self.client_credentials_manager)
    self.token = self.get_spotify_token()

  def get_spotify_token(self):
    # Encode the credentials in base64
    credentials = base64.b64encode(
      f"{self.client_id}:{self.client_secret}".encode()).decode()

    headers = {"Authorization": f"Basic {credentials}"}

    data = {"grant_type": "client_credentials"}

    response = requests.post("https://accounts.spotify.com/api/token",
                             headers=headers,
                             data=data)
    response.raise_for_status()

    return response.json()["access_token"]

  def get_recommendations_from_genre(self, seed_genres):
    limit = len(seed_genres)*4

    base_url = "https://api.spotify.com/v1/recommendations"
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": f"Bearer {self.token}"
    }
    params = {"seed_genres": ','.join(seed_genres), "limit": limit}

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code != 200:
      raise Exception(
        f"Request failed with status code {response.status_code}")

    data = response.json()
    tracks = data['tracks']

    return tracks

  def get_track_details(self, track_id):
    # Get the track details
    track = self.sp.track(track_id)

    # Get the preview URL
    preview_url = track['preview_url']

    # Get the Spotify song URL
    spotify_url = track['external_urls']['spotify']

    # Get the image of the song
    image_url = track['album']['images'][0]['url']

    return preview_url, spotify_url, image_url

  def get_track_features(self, track_id):
    # Get the audio features for the track
    audio_features = self.sp.audio_features([track_id])[0]

    # Extract the desired attributes
    danceability = audio_features['danceability']
    energy = audio_features['energy']
    key = audio_features['key']
    loudness = audio_features['loudness']
    mode = audio_features['mode']
    speechiness = audio_features['speechiness']
    acousticness = audio_features['acousticness']
    instrumentalness = audio_features['instrumentalness']
    liveness = audio_features['liveness']
    valence = audio_features['valence']
    tempo = audio_features['tempo']

    return danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo
