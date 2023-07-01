from http.server import BaseHTTPRequestHandler
import json
import random
import pandas as pd
import numpy as np
import joblib
import pickle
from spotify import spotify
from model import GenrePredictor

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
predictor = GenrePredictor()

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        song_info = data.get('track')

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

        seed_genres = random.sample(genre_dict.get(genre_category[0], []), 5)

        tracks_info = []

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

                if len(tracks_info) >= 3:
                    break

        data = {"tracks": tracks_info}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        return
