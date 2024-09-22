from flask import Blueprint, redirect, request, jsonify, session, url_for
import requests
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv
import os

from utils import get, post, base64_encode

auth = Blueprint('auth', __name__)

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
STATE = os.getenv('STATE')

REDIRECT_URI = 'http://127.0.0.1:5000/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1'

@auth.route('/login')
def login():
    scope = 'user-read-private user-read-email playlist-modify-public playlist-modify-private'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'state': STATE,
        'scope': scope,
        'show_dialog': True
    }

    auth_url = f'{AUTH_URL}?{urllib.parse.urlencode(params)}'

    return redirect(auth_url)

@auth.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({'error': request.args['error']})
    
    if 'code' in request.args:
        code = request.args['code']

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        }

        base64_client_str = base64_encode(f'{CLIENT_ID}:{CLIENT_SECRET}')

        headers = {
            'Authorization': f'Basic {base64_client_str}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(TOKEN_URL, headers=headers, data=data)
        if response.status_code != 201:
            response.raise_for_status()

        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        session['refresh_token'] = token_info['refresh_token']

    return redirect(url_for('views.home'))

@auth.route('/refresh-token')
def refresh_token():
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': session['refresh_token']
    }

    base64_client_str = base64_encode(f'{CLIENT_ID}:{CLIENT_SECRET}')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {base64_client_str}'
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    if response.status_code != 201:
        response.raise_for_status()
            
    new_token_info = response.json()

    session['access_token'] = new_token_info['access_token']
    session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

    return redirect(url_for('views.merge'))

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.home'))