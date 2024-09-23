import sqlite3

def create_database():
    conn = sqlite3.connect('tracks.db')
    cursor = conn.cursor()

    query = '''
        CREATE TABLE IF NOT EXISTS tracks (
            id TEXT PRIMARY_KEY,
            name TEXT,
            artists TEXT,
            acousticness REAL,
            danceability REAL,
            energy REAL,
            instrumentalness REAL,
            key INTEGER,
            liveness REAL,
            loudness REAL,
            mode INTEGER,
            speechiness REAL,
            tempo REAL,
            time_signature INTEGER,
            valence REAL
        );
    '''

    cursor.execute(query)

    conn.commit()
    conn.close()

def add_one(track_data):
    conn = sqlite3.connect('tracks.db')
    cursor = conn.cursor()

    query = 'INSERT INTO tracks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

    cursor.execute(query, (
        track_data['id'], track_data['name'], track_data['artists'],
        track_data['acousticness'], track_data['danceability'], track_data['energy'],
        track_data['instrumentalness'], track_data['key'], track_data['liveness'],
        track_data['loudness'], track_data['mode'], track_data['speechiness'],
        track_data['tempo'], track_data['time_signature'], track_data['valence'],
    ))

    conn.commit()
    conn.close()

def add_many(tracks_data):
    tracks_tuples = [
        (
            track['id'],
            track['name'],
            track['artists'],
            track['acousticness'],
            track['danceability'],
            track['energy'],
            track['instrumentalness'],
            track['key'],
            track['liveness'],
            track['loudness'],
            track['mode'],
            track['speechiness'],
            track['tempo'],
            track['time_signature'],
            track['valence']
        )
        for track in tracks_data
    ]

    conn = sqlite3.connect('tracks.db')
    cursor = conn.cursor()

    query = 'INSERT INTO tracks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    cursor.executemany(query, (tracks_tuples))

    conn.commit()
    conn.close()

def get_all():
    conn = sqlite3.connect('tracks.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tracks')
    items = cursor.fetchall()

    conn.close()

    return items

if __name__ == '__main__':
    items = get_all()
    for item in items:
        print(item)