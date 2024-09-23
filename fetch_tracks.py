'''
- Fetch tracks from multiple endpoints for variety
- Need list of Spotify IDs for the tracks
- List of feature vectors
'''
import requests
from dotenv import load_dotenv
import os
from datetime import datetime

from utils import base64_encode

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
STATE = os.getenv('STATE')

REDIRECT_URI = 'http://127.0.0.1:5000/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1'

class TrackFetcher:
    def __init__(self):
        self.access_token, self.expires_at = self._get_access_token()
    
    def get_all_tracks(self):
        track_data = []

        track_data.extend(self._fetch_new_releases())

        return track_data

    def _fetch_new_releases(self):
        '''
        Returns list of dicts of tracks_data
        '''
        self._check_access_token()
        tracks_data = []

        # Getting newly released albums
        params = {'limit': 50}
        new_albums_response = self._get('/browse/new-releases', params)
        album_ids = [item['id'] for item in new_albums_response['albums']['items']]

        # Creating a dict where key is a track's id and value is the track's info
        tracks_metadata = {}
        for id in album_ids:
            album_tracks = self._get(f'/albums/{id}/tracks')
            for item in album_tracks['items']:
                metadata = {
                    'name': item['name'],
                    'artists': ', '.join([artist['name'] for artist in item['artists']])
                }
                tracks_metadata[item['id']] = metadata

        # Getting every track's audio features and combining it w/ track's info
        ids = list(tracks_metadata.keys())
        for i in range(0, len(ids), 100):
            ids_list = ids[i:i+100]
            ids_string = ','.join(ids_list)
            params = {'ids': ids_string}
            response = self._get(f'/audio-features', params)

            batch_data = response['audio_features']
            for e in batch_data:
                e.update(tracks_metadata[e['id']])
                
            tracks_data.extend(batch_data)
        
        return tracks_data

    def _check_access_token(self):
        if datetime.now().timestamp() >= self.expires_at:
            self.access_token, self.expires_at = self._get_access_token()

    def _get_access_token(self):
        base64_client_str = base64_encode(f'{CLIENT_ID}:{CLIENT_SECRET}')
        headers = {
            'Authorization': f'Basic {base64_client_str}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'client_credentials'
        }

        response = requests.post(TOKEN_URL, headers=headers, data=data)
        if response.status_code != 200:
            response.raise_for_status()

        response_dict = response.json()

        access_token = response_dict.get('access_token')
        expires_at = datetime.now().timestamp() + response_dict['expires_in']

        return access_token, expires_at

    def _get(self, endpoint, params=None):
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = requests.get(f'{API_BASE_URL}{endpoint}', headers=headers, params=params)
        if response.status_code != 200:
            response.raise_for_status()

        return response.json()