# Zot Music
Zot Music is a web application that builds on Spotify's user experience with a unique playlist management tool and music recommendation tool.

## Installation
1. Clone the repo
    ```bash
    git clone https://github.com/carsonmdd/Zot-Music.git
    ```
2. Navigate to project directory
    ```bash
    cd Zot-Music
    ```
3. (Optional) Use a virtual environment to avoid installing dependencies globally.
- Create a virtual environment:
    ```bash
    python -m venv .venv
    ```
- Activate the virutal environment:
    - macOS:
        ```bash
        source .venv/bin/activate
        ```
    - Windows:
        ```bash
        .venv/Scripts/activate
        ```
4. Install the required dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Usage
### Running the app
```bash
python main.py
```

### Merging playlists
Zot Music provides the ability to merge two public playlists with duplicates removed from a user's Spotify library.
1. Log in with Spotify.
2. Once logged in, click "Merge Playlists."
3. Select two playlists to merge and click the "Merge" button to view the resulting tracks on the right.
4. Optionally enter a title for the new playlist and click "Save to profile" to save the new playlist to your Spotify profile.

### Getting recommendations
Music recommendations can be generated based on a selected track.
1. Log in with Spotify.
2. Once logged in, click "Recommendations."
3. Enter a track name to search for and select the correct track from the displayed search results.
4. Click "Get recommendations" to view the top track recommendations on the right.
