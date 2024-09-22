from flask import Blueprint, session, redirect, jsonify, render_template, url_for, request
import requests
from datetime import datetime

from utils import get, post

views = Blueprint('views', __name__)

API_BASE_URL = 'https://api.spotify.com/v1'

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/merge', methods=['GET', 'POST'])
def merge():
    if request.method == 'POST':
        '''
        - Get two playlist ids
        - Create a set of the playlists' tracks' URIs
        - Create new playlist
        - Add set of URIs to new playlist
        '''
        id1 = request.form['playlist-1']
        id2 = request.form['playlist-2']

        uri_set = set()
        p1_uris = get_uris(id1)
        p2_uris = get_uris(id2)
        uri_set.update(p1_uris)
        uri_set.update(p2_uris)

        user_id = get_user_id()
        playlist_id = create_playlist(user_id)

        add_uris(playlist_id, list(uri_set))

    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    if datetime.now().timestamp() > session['expires_at']:
        return redirect(url_for('auth.refresh_token'))

    data = get(session['access_token'], '/me/playlists')
    playlists = data['items']

    return render_template('merge.html', playlists=playlists)

def get_uris(id):
    uris = []

    url = f'{API_BASE_URL}/playlists/{id}/tracks'
    offset = 0
    headers = {'Authorization': f'Bearer {session['access_token']}'}
    params = {'limit': 50, 'offset': offset}
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 201:
            response.raise_for_status()
        
        data = response.json()
        uris.extend([item['track']['uri'] for item in data['items']])

        url = data['next']
        offset += 50

    return uris

def get_user_id():
    data = get(session['access_token'], '/me')
    return data['id']

def create_playlist(user_id):
    data = {
        'name': 'Coolest playlist',
        'description': 'This is the coolest playlist ever!'
    }
    response_data = post(session['access_token'], f'/users/{user_id}/playlists', data)

    return response_data['id']

def add_uris(id, uris):
    for i in range(0, len(uris), 100):
        data = {'uris': uris[i:i+100]}
        post(session['access_token'], f'/playlists/{id}/tracks', data)

@views.route('/recommend', methods=['GET', 'POST'])
def recommend():
    '''
    - User types in track name to search
    - Form submits post request with track name to search for
    - App shows search results and user selects track
    - Form submits post request with track id
    - App gets audio features for track
    - App performs cosine similarity with track and all tracks in database and shows 5 highest scores
    '''

    # id = 12345
    # track_data = get_track_data(id)
    # rec = Recommender()
    # rec.get_recommendations(track_data)

    return render_template('recommend.html')