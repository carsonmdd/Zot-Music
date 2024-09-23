import database as db
from utils import get
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:
    def __init__(self, access_token):
        self.access_token = access_token
    
    def recommend(self, track_id):
        s_track = self._create_s_track(track_id)

        db_tracks = db.get_all()
        similarities = self._compute_similarities(s_track, db_tracks)

        similarities.sort(key=lambda x: x[1], reverse=True)
        # for similarity in similarities[:5]:
        #     print(similarity)
        top_5_tracks = [similarity[0] for similarity in similarities[:5]]
        
        return top_5_tracks
    
    def _create_s_track(self, track_id):
        endpoint = f'/tracks/{track_id}'
        track_info = get(self.access_token, endpoint)

        endpoint = f'/audio-features/{track_id}'
        s_track_audio_features = get(self.access_token, endpoint)

        s_track = (
            track_id,
            track_info['name'],
            ', '.join([artist['name'] for artist in track_info['artists']]),
            s_track_audio_features['acousticness'],
            s_track_audio_features['danceability'],
            s_track_audio_features['energy'],
            s_track_audio_features['instrumentalness'],
            s_track_audio_features['key'],
            s_track_audio_features['liveness'],
            s_track_audio_features['loudness'],
            s_track_audio_features['mode'],
            s_track_audio_features['speechiness'],
            s_track_audio_features['tempo'],
            s_track_audio_features['time_signature'],
            s_track_audio_features['valence']
        )

        return s_track

    def _compute_similarities(self, s_track, db_tracks):
        s_audio_features = s_track[3:]
        s_feature_vector = np.array([s_audio_features])

        similarities = []
        for track in db_tracks:
            if s_track[0] == track[0]:
                continue

            audio_features = track[3:]
            feature_vector = np.array([audio_features])
            similarity = cosine_similarity(s_feature_vector, feature_vector)[0][0]
            similarities.append((track, similarity))

        return similarities