import os
from tkinter import NO
from dotenv import load_dotenv
from requests import session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from atproto import Client



#  #### Spotify Utils ####
def init_spotipy():
    """
    Initialize spotipy object with user credentials
    """
    # Load credentials
    # with open('credentials.json') as f:
    #     credentials = json.load(f)
    # Initialize spotipy object
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                                                   client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                                                   redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
                                                   scope='user-read-currently-playing',
                                                   cache_path=os.getenv('SPOTIFY_CACHE_PATH')
                                                   ))
    return sp

def get_track_info(track):
    if track and track['item']:
        return {
            "title": track['item']['name'],
            "artist": track['item']['artists'][0]['name'],
            "url": track['item']['external_urls']['spotify']
        }
    else:
        return None

def get_last_10_tracks(sp):
    recent_tracks = sp.current_user_recently_played(limit=10)

    for idx, item in enumerate(recent_tracks['items']):
        track = item['track']
        print(f"{idx + 1}: {track['name']} by {track['artists'][0]['name']}")


def get_now_playing(sp, currentTrack):
    track = sp.current_user_playing_track()     # Get track info
    if track and track['item']:
        duration = track['item']['duration_ms'] # in milliseconds
        progress = track['progress_ms']
        if progress < duration * 0.25:
            currentTrack = track
            # in seconds
        return currentTrack, duration, progress
    else:
        return None, 999999, 0
