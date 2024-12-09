import os, time
from pickletools import read_stringnl_noescape
from httpx import ReadTimeout
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from atproto import Client
from bsky_utils import post_tracks


#########
# Initialization and setup
#########
def run_test_mode():
    listened = []
    print("Test mode: Enabled")
    # Simulate adding tracks to the listened list
    n = 10
    for i in range(3):
        track_info = {
            "title": f"Test Track {i+n}",
            "artist": f"Test Artist {i+n}",
            "url": f"http://example.com/track{i+n}"
        }
        listened.append(track_info)
    # Post the simulated tracks
    if not post_tracks(listened):
        print("Error: Could not post tracks to Bluesky")
        return
    print("Test mode: Posted simulated tracks")
    return

def update_details():
    with open(".env", "w") as f:
        spotify_client_id = input("Enter Spotify Client ID: ")
        spotify_client_secret = input("Enter Spotify Client Secret: ")
        bluesky_handle = input("Enter Bluesky Handle: ")
        bluesky_password = input("Enter Bluesky Password: ")
        f.write(f"SPOTIFY_CLIENT_ID={spotify_client_id}\n")
        f.write(f"SPOTIFY_CLIENT_SECRET={spotify_client_secret}\n")
        f.write(f"SPOTIFY_REDIRECT_URI={os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:1234')}\n")
        f.write(f"SPOTIFY_SCOPE={os.getenv('SPOTIFY_SCOPE', 'user-read-currently-playing')}\n")
        f.write(f"SPOTIFY_CACHE_PATH={os.getenv('SPOTIFY_CACHE_PATH', '.cache')}\n")
        f.write(f"BLUESKY_HANDLE={bluesky_handle}\n")
        f.write(f"BLUESKY_PASSWORD={bluesky_password}\n")
        print("Environment variables saved to .env file")


########
#  #### Spotify Utils ####
def init_spotipy():
    """
    Initialize a Spotipy object with user credentials.

    This function sets up the Spotipy client using OAuth authentication. 
    It retrieves the necessary credentials from environment variables and 
    initializes the Spotipy object with these credentials.

    Returns:
        spotipy.Spotify: An authenticated Spotipy client object.
    """
    if not os.getenv('SPOTIFY_CLIENT_ID') or not os.getenv('SPOTIFY_CLIENT_SECRET'):
        raise spotipy.SpotifyException(400, -1, "Missing Spotify credentials")
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
                scope='user-read-currently-playing',
                cache_path=os.getenv('SPOTIFY_CACHE_PATH')
                ))
    except spotipy.SpotifyException as e:
        print(f"Error initialising Spotify: {e}")
        raise
    return sp


def get_track_info(track):
    """
    Extracts track information from a given track dictionary.

    Args:
        track (dict): A dictionary containing track information. Expected to have an 'item' key with nested details.

    Returns:
        dict: A dictionary containing the track's title, artist, and Spotify URL if the track and 'item' key are present.
        None: If the track or 'item' key is not present.
    """
    if track and track['item']:
        return {
            "title": track['item']['name'],
            "artist": track['item']['artists'][0]['name'],
            "url": track['item']['external_urls']['spotify']
        }
    else:
        return None


def get_now_playing(sp, currentTrack):
    """
    Retrieves the currently playing track information from the Spotify API.

    Args:
        sp (spotipy.Spotify): An authenticated Spotify client instance.
        currentTrack (dict): A dictionary to store the current track information.

    Returns:
        tuple: A tuple containing:
            - currentTrack (dict or None): The current track information if a track is playing, otherwise None.
            - duration (int): The duration of the track in milliseconds, or 999999 if no track is playing.
            - progress (int): The progress of the track in milliseconds, or 0 if no track is playing.
    """
    retries = 3
    for attempt in range(retries):
        try:
            track = sp.current_user_playing_track()     # Get track info
            if track and track['item']:
                duration = track['item']['duration_ms'] # in milliseconds
                progress = track['progress_ms']
                if progress < duration * 0.25:
                    currentTrack = track
                return currentTrack, duration, progress
            return (None, 999999, 0)
        except ReadTimeout:
            if attempt < retries - 1:
                print(f"Read timeout occurred. Retrying... ({attempt + 1}/{retries})")
                time.sleep(5)  # Wait for 2 seconds before retrying
            else:
                print("Read timeout occurred. Max retries reached.")
                raise
        except spotipy.SpotifyException as e:
            print(f"Error getting current track: {e}")
            raise

