from http.server import BaseHTTPRequestHandler
import json
import random
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

    def do_GET(self):
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

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        return
