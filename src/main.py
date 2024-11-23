import time

from utils import get_config, init_spotipy
# from spotify_utils import get_now_playing
from atproto import Client, client_utils
from utils import get_config

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
    timeRemaining = 30     # seconds
    client = Client()
    print(client)
    client.login(config['bluesky']['handle'], config['bluesky']['password'])
    listened = []
    while True:
        track = sp.current_user_playing_track()     # Get track info
        print(track)
        if track and track['item']:
            duration = track['item']['duration_ms'] # in milliseconds
            progress = track['progress_ms']
            if progress < duration * 0.25:
                currentTrack = track

        if currentTrack and progress >= duration * 0.75:
            trackInfo = get_track_info(currentTrack)
            listened.append(trackInfo)
            currentTrack = None

            # if trackInfo and trackInfo['title'] not in listened:
            #     listened.append(trackInfo['title'])
            #     post_now_playing(client, trackInfo)
        
        if len(listened) >= 3:
            post_tracks(client, listened)
            listened = []
        time.sleep(5)


if __name__ == "__main__":
    main()