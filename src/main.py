import re
import time

import spotipy

from utils import get_config, init_spotipy
# from spotify_utils import get_now_playing
from atproto import Client, client_utils
from bsky_utils import post_now_playing, post_tracks


# Load config
config = get_config()
# Bluesky client
client = Client()
client.login(config['bluesky']['handle'], config['bluesky']['password'])


def get_track_info(track):
    if track and track['item']:
        return {
            "title": track['item']['name'],
            "artist": track['item']['artists'][0]['name'],
            "url": track['item']['external_urls']['spotify']
        }
    else:
        return None


def main():

    sp = init_spotipy(config)
    currentTrack = None
    client = Client()
    print(client)
    client.login(config['bluesky']['handle'], config['bluesky']['password'])
    listened = []
    while True:
        try:
            track = sp.current_user_playing_track()     # Get track info
            print(track)
            if track and track['item']:
                duration = track['item']['duration_ms'] # in milliseconds
                progress = track['progress_ms']
                if progress < duration * 0.25:
                    currentTrack = track
            
            # ToDo: Should I prevent tracks being repeated?
            if currentTrack and progress >= duration * 0.75:
                trackInfo = get_track_info(currentTrack)
                listened.append(trackInfo)
                currentTrack = None

            
            if len(listened) >= 3:
                post_tracks(client, listened)
                listened = []

            remainingTime = (duration - progress) / 1000    # in seconds
            time.sleep(min(remainingTime, 10))
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                retryAfter = int(e.headers.get('Retry-After', 10))
                print(f"Rate limited. Retrying in {retryAfter} seconds")
                time.sleep(retryAfter)
            else:
                print(f"Error: {e}")
                time.sleep(10)


if __name__ == "__main__":
    main()