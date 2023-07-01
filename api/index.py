from flask import Flask, jsonify, request
from spotify import spotify
from model import GenrePredictor
from flask_cors import CORS
import pandas as pd
import random

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


@app.route('/api/get-chosen-song-give-reccomended-songs', methods=['POST'])
def get_chosen_song_give_reccomended_songs():
    data = request.get_json()
    print(data)
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
    
    print(genre_category)

    # Select five random genres from the predicted category
    seed_genres = random.sample(genre_dict.get(genre_category[0], []), 5)

    # List to store track features
    tracks_info = []

# Keep fetching recommendations until we have at least 3 so ngs
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

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000)
    
# if __name__ == '__main__':
#     app.run(debug=True)
