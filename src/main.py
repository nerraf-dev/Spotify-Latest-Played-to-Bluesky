import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from atproto import Client
import json

with open('src/config.json') as f:
    config = json.load(f)

sp_client_id = config['spotify']['client_id']
sp_client_secret = config['spotify']['client_secret']
sp_redirect_uri = config['spotify']['redirect_uri']
bsky_handle = config['bluesky']['handle']
bsky_password = config['bluesky']['password']

def get_now_playing(track):
    # current = sp.current_user_playing_track()
    if track and track['item']:
        return {
            "title": track['item']['name'],
            "artist": track['item']['artists'][0]['name'],
            "url": track['item']['external_urls']['spotify']
        }
    else:
        return None
    
# def get_all_track_info(sp):
#     current = sp.current_user_playing_track()
#     if current:
#         return current
#     else:
#         return None

def post_current_track(client, track):
    post = f"Now Playing: {track['title']} by {track['artist']} - url: {track['url']}"
    client.send_post(post)
    print(post)

def get_last_10_tracks(sp):
    recent_tracks = sp.current_user_recently_played(limit=10)

    for idx, item in enumerate(recent_tracks['items']):
        track = item['track']
        print(f"{idx + 1}: {track['name']} by {track['artists'][0]['name']}")

def get_time_remaining(track):
    if track:
        return track['item']['duration_ms'] - track['progress_ms']
    else:
        return None



def main():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=sp_client_id,
    client_secret=sp_client_secret,
    redirect_uri=sp_redirect_uri,
    scope="user-library-read user-read-playback-state user-read-recently-played",
    cache_path=".cache"
    ))

    client = Client()
    client.login(bsky_handle, bsky_password)

    current_track = None
    time_remaining = 30
    while True:
        track = sp.current_user_playing_track()
        if track and track['item']:

            duration = track['item']['duration_ms']
            time_remaining = max(0, duration - track['progress_ms'])/1000 # in seconds
            print(f"time remaining: {time_remaining}")
            now_playing = get_now_playing(track)
            if now_playing != current_track:
                post_current_track(client, now_playing)
                # print(now_playing)
                current_track = now_playing
            else:
                print("No change in track")
        else:
            print("No track currently playing")
            time_remaining = 30
        time.sleep(time_remaining)


if __name__ == "__main__":
    main()