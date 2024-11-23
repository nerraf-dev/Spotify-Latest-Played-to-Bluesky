import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


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
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope='user-read-currently-playing',
            cache_path=os.getenv('SPOTIFY_CACHE_PATH')
            ))
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
    track = sp.current_user_playing_track()     # Get track info
    if track and track['item']:
        duration = track['item']['duration_ms'] # in milliseconds
        progress = track['progress_ms']
        if progress < duration * 0.25:
            currentTrack = track
            # in seconds
        return currentTrack, duration, progress
    else:
        return (None, 999999, 0)
