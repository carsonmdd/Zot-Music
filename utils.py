import requests
import base64

API_BASE_URL = 'https://api.spotify.com/v1'

def get(token, endpoint, params=None):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{API_BASE_URL}{endpoint}', headers=headers, params=params)
    if response.status_code != 201:
        response.raise_for_status()

    return response.json()

def post(token, endpoint, data):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f'{API_BASE_URL}{endpoint}', headers=headers, json=data)

    if response.status_code != 201:
        response.raise_for_status()

    return response.json()

def base64_encode(s: str) -> str:
    s_bytes = s.encode('ascii')

    base64_bytes = base64.b64encode(s_bytes)
    base64_str = base64_bytes.decode('ascii')

    return base64_str