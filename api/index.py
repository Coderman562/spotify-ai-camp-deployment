from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import random

import joblib
import pandas as pd
import os

# class GenrePredictor:
#     def __init__(self):
#         # Get the absolute path of the directory where app.py is located
#         dir_path = os.path.dirname(os.path.realpath(__file__))

#         # Use the absolute path to load the model
#         model_path = os.path.join(dir_path, 'trained_model_xgboost_v2.joblib')
#         self.model = joblib.load(model_path)

#         # Use the absolute path to load the label encoder
#         encoder_path = os.path.join(dir_path, 'label_encoder_v2.joblib')
#         self.label_encoder = joblib.load(encoder_path)

#     def predict_genre(self, input_data):
#         print(input_data.head())
#         # Select the non-numerical columns
#         non_numerical_cols = input_data.select_dtypes(include=['object']).columns
        
#         print(non_numerical_cols)

#         # Perform one-hot encoding on the non-numerical columns
#         input_data_encoded = pd.get_dummies(input_data, columns=non_numerical_cols)
        
#         print(input_data_encoded)

#         # Standardize the features
#         # scaler = StandardScaler()
#         # input_data_scaled = scaler.fit_transform(input_data_encoded)

#         # Make predictions on the input data
#         y_pred_encoded = self.model.predict(input_data)
        
#         print(y_pred_encoded)

#         # Inverse transform the encoded predictions
#         y_pred = self.label_encoder.inverse_transform(y_pred_encoded)

#         return y_pred


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


genre_dict = {
    "Rock/Alternative/Punk/Metal": ["alt-rock", "alternative", "black-metal", "death-metal", "emo", "folk", "goth", "grunge", "hard-rock", "hardcore", "heavy-metal", "indie", "indie-pop", "metal", "metal-misc", "metalcore", "punk", "punk-rock", "rock", "rock-n-roll", "rockabilly"],
    "Electronic/Dance/Techno": ["afrobeat", "breakbeat", "chicago-house", "club", "dance", "dancehall", "deep-house", "detroit-techno", "disco", "drum-and-bass", "dub", "dubstep", "edm", "electro", "electronic", "garage", "house", "idm", "minimal-techno", "post-dubstep", "progressive-house", "techno", "trance", "trip-hop"],
    "Pop/Disco/Funk/R&B": ["cantopop", "disney", "funk", "j-dance", "j-idol", "j-pop", "k-pop", "latin", "latino", "mandopop", "philippines-opm", "pop", "pop-film", "power-pop", "r-n-b", "reggaeton", "salsa", "samba", "sertanejo", "soul", "synth-pop"],
    "Country/Jazz/Blues/Classical": ["acoustic", "bluegrass", "blues", "bossanova", "brazil", "british", "country", "classical", "french", "gospel", "honky-tonk", "indian", "iranian", "jazz", "new-age", "opera", "piano", "show-tunes", "singer-songwriter", "spanish", "tango", "turkish", "world-music"]
}

# Spotify details
client_id = 'f74d125a75774bb886fea891b2324a1a'
client_secret = '4f5e9dc1a61e442bb5f6d3aa83b4d185'

s = spotify(client_id, client_secret)
# predictor = GenrePredictor()

app = Flask(__name__)
CORS(app)

#@app.route('/')
#def index():
#    return "Hello, this is my Flask app!"

@app.route('/api/get-5-songs', methods=['GET'])
def get_5_songs():
    while True:
        # Randomly select a genre category
        genre_category = random.choice(list(genre_dict.keys()))

        # Randomly select three genres from the chosen category
        seed_genres = random.sample(genre_dict[genre_category], 5)

        recommendations = s.get_recommendations_from_genre(seed_genres)

        # List to store track features
        tracks_info = []

        for track in recommendations:
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            preview_url = track['preview_url']
            spotify_url = track['external_urls']['spotify']
            track_image = track['album']['images'][0]['url'] if track['album']['images'] else None
            track_id = track['id']
            explicit = track['explicit']
            danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo = s.get_track_features(track_id)

            # Check if preview_url is not None or empty
            if preview_url:
                track_features = {
                    'trackName': track_name,
                    'artistName': artist_name,
                    'previewUrl': preview_url,
                    'spotifyUrl': spotify_url,
                    'trackImage': track_image,
                    'trackId': track_id,
                    'Explicit': explicit,
                    'Danceability': danceability,
                    'Energy': energy,
                    'Key': key,
                    'Loudness': loudness,
                    'Mode': mode,
                    'Speechiness': speechiness,
                    'Acousticness': acousticness,
                    'Instrumentalness': instrumentalness,
                    'Liveness': liveness,
                    'Valence': valence,
                    'Tempo': tempo
                }

                tracks_info.append(track_features)

        if len(tracks_info) >= 5:
            break

    data = {"tracks": tracks_info}
    return jsonify(data)


# @app.route('/api/get-chosen-song-give-reccomended-songs', methods=['POST'])
# def get_chosen_song_give_reccomended_songs():
#     data = request.get_json()
#     print(data)
#     song_info = data.get('track')

#     track_features = {
#         'explicit': song_info.get('explicit'),
#         'danceability': song_info.get('danceability'),
#         'energy': song_info.get('energy'),
#         'key': song_info.get('key'),
#         'loudness': song_info.get('loudness'),
#         'mode': song_info.get('mode'),
#         'speechiness': song_info.get('speechiness'),
#         'acousticness': song_info.get('acousticness'),
#         'instrumentalness': song_info.get('instrumentalness'),
#         'liveness': song_info.get('liveness'),
#         'valence': song_info.get('valence'),
#         'tempo': song_info.get('tempo')
#     }

#     df = pd.DataFrame.from_dict([track_features])
#     genre_category = predictor.predict_genre(df)
    
#     print(genre_category)

#     # Select five random genres from the predicted category
#     seed_genres = random.sample(genre_dict.get(genre_category[0], []), 5)

#     # List to store track features
#     tracks_info = []

# # Keep fetching recommendations until we have at least 3 so ngs
#     while len(tracks_info) < 3:
#         recommendations = s.get_recommendations_from_genre(seed_genres)

#         for track in recommendations:
#             track_name = track['name']
#             artist_name = track['artists'][0]['name']
#             preview_url = track['preview_url']
#             spotify_url = track['external_urls']['spotify']
#             track_image = track['album']['images'][0]['url'] if track['album']['images'] else None
#             track_id = track['id']
#             explicit = track['explicit']
#             danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo = s.get_track_features(track_id)

#             # Check if preview_url is not None or empty
#             if preview_url:
#                 track_features = {
#                     'trackName': track_name,
#                     'artistName': artist_name,
#                     'previewUrl': preview_url,
#                     'spotifyUrl': spotify_url,
#                     'trackImage': track_image,
#                     'trackId': track_id,
#                     'Explicit': explicit,
#                     'Danceability': danceability,
#                     'Energy': energy,
#                     'Key': key,
#                     'Loudness': loudness,
#                     'Mode': mode,
#                     'Speechiness': speechiness,
#                     'Acousticness': acousticness,
#                     'Instrumentalness': instrumentalness,
#                     'Liveness': liveness,
#                     'Valence': valence,
#                     'Tempo': tempo
#                 }

#                 tracks_info.append(track_features)

#             # Break the loop if we have at least 3 songs
#             if len(tracks_info) >= 3:
#                 break

#     print(tracks_info)
#     data = {"tracks": tracks_info}
#     return data

@app.route('/api/1')
def example():
   return "Hello, this is my Flask app!"

@app.route('/api/2')
def example2():
   return "Hello, this is my Flask app!"

@app.route('/api/3')
def example3():
   return "Hello, this is my Flask app!"

@app.route('/api/4')
def example4():
   return "Hello, this is my Flask app!"

@app.route('/api/5')
def example5():
   return "Hello, this is my Flask app!"

@app.route('/api/6')
def example6():
   return "Hello, this is my Flask app!"

@app.route('/api/7')
def example7():
   return "Hello, this is my Flask app!"

@app.route('/api/8')
def example8():
   return "Hello, this is my Flask app!"

@app.route('/api/9')
def example9():
   return "Hello, this is my Flask app!"

@app.route('/api/10')
def example10():
   return "Hello, this is my Flask app!"

@app.route('/api/11')
def example11():
   return "Hello, this is my Flask app!"

@app.route('/api/12')
def example12():
   return "Hello, this is my Flask app!"

@app.route('/api/13')
def example13():
   return "Hello, this is my Flask app!"

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
    
# if __name__ == '__main__':
#     app.run(debug=True)

