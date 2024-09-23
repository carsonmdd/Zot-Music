from flask import Blueprint, session, redirect, render_template, url_for, request
import requests
from datetime import datetime

from utils import get, post
from recommender import Recommender

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
    tracks = []
    if request.method == 'POST':
        '''
        - Get two playlist ids
        - Create a set of the playlists' tracks' URIs
        - Create new playlist
        - Add set of URIs to new playlist
        '''
        id1 = request.form['playlist-1']
        id2 = request.form['playlist-2']

        p1_tracks = _get_tracks(id1)
        p2_tracks = _get_tracks(id2)
        all_tracks = p1_tracks + p2_tracks
        uris_set = set()
        for track in all_tracks:
            if track['uri'] not in uris_set:
                uris_set.add(track['uri'])
                tracks.append(track)

        session['uris'] = list(uris_set)

    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    if datetime.now().timestamp() > session['expires_at']:
        return redirect(url_for('auth.refresh_token'))

    data = get(session['access_token'], '/me/playlists')
    playlists = data['items']

    return render_template('merge.html', playlists=playlists, tracks=tracks)

def _get_tracks(id):
    tracks = []

    url = f'{API_BASE_URL}/playlists/{id}/tracks'
    offset = 0
    headers = {'Authorization': f'Bearer {session['access_token']}'}
    params = {'limit': 50, 'offset': offset}
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 201:
            response.raise_for_status()
        
        data = response.json()
        tracks.extend([item['track'] for item in data['items']])

        url = data['next']
        offset += 50

    return tracks

@views.route('/save-to-profile', methods=['POST'])
def save_to_profile():
    user_id = _get_user_id()
    playlist_id = _create_playlist(user_id, request.form['title'])

    _add_tracks(playlist_id, session['uris'])

    return redirect('/merge')

def _get_user_id():
    data = get(session['access_token'], '/me')
    return data['id']

def _create_playlist(user_id, title):
    data = {'name': title}
    response_data = post(session['access_token'], f'/users/{user_id}/playlists', data)

    return response_data['id']

def _add_tracks(id, uris):
    for i in range(0, len(uris), 100):
        data = {'uris': uris[i:i+100]}
        post(session['access_token'], f'/playlists/{id}/tracks', data)

@views.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    uri = request.form['selected-track']
    r = Recommender(uri)
    tracks = r.recommend()

    redirect('/recommendations')

@views.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
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

    search_tracks = []
    rec_tracks = []
    if request.method == 'POST':
        if 'search-query' in request.form:
            search_tracks = search(request.form['search-query'])
        elif 'selected-track' in request.form:
            rec = Recommender()
            rec_tracks = rec.recommend(request.form['selected-track'])

    return render_template('recommendations.html', search_tracks=search_tracks, rec_tracks=rec_tracks)

def search(search_query):
    endpoint = '/search'
    params = {
        'q': search_query,
        'type': 'track',
    }
    data = get(session['access_token'], endpoint, params)
    tracks = data['tracks']['items']
    for track in tracks:
        track['artists'] = ', '.join([artist['name'] for artist in track['artists']])

    return tracks