from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import random

import joblib
import pandas as pd
import os

#import sys
#from pathlib import Path
#sys.path.insert(0, str(Path(__file__).resolve()))
import sys
from pathlib import Path
sys.path.insert(0, "api")

import logging

# Set up the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO)


from spotify import spotify
from model import GenrePredictor

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests
import base64

client_id = 'f74d125a75774bb886fea891b2324a1a'
client_secret = '4f5e9dc1a61e442bb5f6d3aa83b4d185'

genre_dict = {
    "Rock/Alternative/Punk/Metal": ["alt-rock", "alternative", "black-metal", "death-metal", "emo", "folk", "goth", "grunge", "hard-rock", "hardcore", "heavy-metal", "indie", "indie-pop", "metal", "metal-misc", "metalcore", "punk", "punk-rock", "rock", "rock-n-roll", "rockabilly"],
    "Electronic/Dance/Techno": ["afrobeat", "breakbeat", "chicago-house", "club", "dance", "dancehall", "deep-house", "detroit-techno", "disco", "drum-and-bass", "dub", "dubstep", "edm", "electro", "electronic", "garage", "house", "idm", "minimal-techno", "post-dubstep", "progressive-house", "techno", "trance", "trip-hop"],
    "Pop/Disco/Funk/R&B": ["cantopop", "disney", "funk", "j-dance", "j-idol", "j-pop", "k-pop", "latin", "latino", "mandopop", "philippines-opm", "pop", "pop-film", "power-pop", "r-n-b", "reggaeton", "salsa", "samba", "sertanejo", "soul", "synth-pop"],
    "Country/Jazz/Blues/Classical": ["acoustic", "bluegrass", "blues", "bossanova", "brazil", "british", "country", "classical", "french", "gospel", "honky-tonk", "indian", "iranian", "jazz", "new-age", "opera", "piano", "show-tunes", "singer-songwriter", "spanish", "tango", "turkish", "world-music"]
}

s = spotify(client_id, client_secret)
# predictor = GenrePredictor()

app = Flask(__name__)
CORS(app)

#@app.route('/')
#def index():
#    return "Hello, this is my Flask app!"

@app.route('/api/get-5-songs', methods=['GET'])
def get_5_songs():
   print("STARTED!")
   logger.info("STARTED!")
   logging.info("STARTED!!!")
   
   s = spotify(client_id, client_secret)

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
#     song_info = data.get('track')

#     s = spotify(client_id, client_secret)

#     print("checkpoint 1")

#     genre_category = random.choice(list(genre_dict.keys()))

#     print(genre_category)

#     # Select five random genres from the predicted category
#     seed_genres = random.sample(genre_dict.get(genre_category, []), 5)

#     print(seed_genres)

#     # List to store track features
#     tracks_info = []

#     # Keep fetching recommendations until we have at least 3 songs
#     while len(tracks_info) < 3:
#         print("checkpoint 2")
#         recommendations = s.get_recommendations_from_genre(seed_genres)

#         for track in recommendations:
#             print("checkpoint 3")
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

#     data = {"tracks": tracks_info}
#     return data

@app.route('/api/get-chosen-song-give-reccomended-songs', methods=['POST'])
def get_chosen_song_give_reccomended_songs():
   data = request.get_json()
   print(data)
   song_info = data.get('track')
   
   s = spotify(client_id, client_secret)
   predictor = GenrePredictor()


   track_features = {
      'explicit': song_info.get('explicit'),
      'danceability': song_info.get('danceability'),
      'energy': song_info.get('energy'),
      'key': song_info.get('key'),
      'loudness': song_info.get('loudness'),
      'mode': song_info.get('mode'),
      'speechiness': song_info.get('speechiness'),
      'acousticness': song_info.get('acousticness'),
      'instrumentalness': song_info.get('instrumentalness'),
      'liveness': song_info.get('liveness'),
      'valence': song_info.get('valence'),
      'tempo': song_info.get('tempo')
   }

   df = pd.DataFrame.from_dict([track_features])
   genre_category = predictor.predict_genre(df)
   
   print(genre_category)

   # Select five random genres from the predicted category
   seed_genres = random.sample(genre_dict.get(genre_category[0], []), 5)

   # List to store track features
   tracks_info = []

   # Keep fetching recommendations until we have at least 3 songs
   while len(tracks_info) < 3:
      recommendations = s.get_recommendations_from_genre(seed_genres)

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

         # Break the loop if we have at least 3 songs
         if len(tracks_info) >= 3:
               break

   print(tracks_info)
   data = {"tracks": tracks_info}
   return data

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

