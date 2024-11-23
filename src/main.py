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
    while True:
        print("check")
        # timeRemaining, currentTrack = get_now_playing(sp, currentTrack, config)
        track = sp.current_user_playing_track()     # Get track info
        print(track)
        if track and track['item']:
            duration = track['item']['duration_ms'] # in milliseconds
            timeRemaining = max(0, duration - track['progress_ms'])/1000 # in seconds
            print(timeRemaining)
            nowPlaying = get_track_info(track)
            if nowPlaying != currentTrack:
                # post_now_playing(client, nowPlaying)
                tb = client_utils.TextBuilder()
                trackInfo = f"{nowPlaying['title']} by {nowPlaying['artist']}\n\n"
                # tb.text(trackInfo)
                tb.text("Now Playing: ")
                tb.link(trackInfo, nowPlaying['url'])
                # client.send_post(tb)
                print(tb)
                currentTrack = nowPlaying
            else:
                print("No change in track")
                timeRemaining = max(0, duration - track['progress_ms'])/1000 # in seconds
                print(timeRemaining)
        else:
            print("No track currently playing")
            timeRemaining = 30
        time.sleep(timeRemaining)


if __name__ == "__main__":
    main()