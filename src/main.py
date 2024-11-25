import time, spotipy, os
from turtle import listen
from dotenv import load_dotenv
from bsky_utils import post_tracks
from utils import (init_spotipy,
                   get_track_info,
                   get_now_playing,
                   run_test_mode, 
                   update_details,
                   check_spotify_details,
                   check_bluesky_details)


def initialise():
    sp = init_spotipy()
    listened = []
    return (sp, None, listened)

def load_configuration():
    if not load_dotenv():
        print("""
            To continue you will need your Spotify Developer Client ID and Client Secret.
            You can create a Spotify Developer account and create a new app to get these credentials.
            You will also need your Bluesky handle and password.
              
            Please enter the required information when prompted.
              Press Enter to continue...
            """)
        input()
        update_details()
        return False
    return True

def main():
    load_configuration()

    print("""
        Listening for tracks...
          
        Press Ctrl+C to exit at any time.
          """)
    
    sp, currentTrack, listened = initialise()
    # Enable test mode
    test_mode = False
    if test_mode:
        run_test_mode()
    else:
        listen_for_tracks(sp, currentTrack, listened)

def listen_for_tracks(sp, currentTrack, listened):
    while True:
        try:
            currentTrack, duration, progress = get_now_playing(sp, currentTrack)
            if(currentTrack):
                print(f"Currently playing: {currentTrack['item']['name']} by {currentTrack['item']['artists'][0]['name']}")
            remainingTime = (duration - progress) / 1000    # in seconds
            if currentTrack and progress >= duration * 0.75:
                trackInfo = get_track_info(currentTrack)
                listened.append(trackInfo)
                currentTrack = None
                print(f"Added track to listened: {trackInfo}")
            if len(listened) >= 3:
                if (listened[0] == listened[1]) and (listened[1] == listened[2]):
                    print("Stuck on repeat")
                post_tracks(listened)
                listened.clear()
            time.sleep(min(remainingTime, 10))
        except spotipy.exceptions.SpotifyException as e:
            handle_spotify_exception(e)

def handle_spotify_exception(e):
    if e.http_status == 429:
        retryAfter = int(e.headers.get('Retry-After', 10))
        print(f"Rate limited. Retrying in {retryAfter} seconds")
        time.sleep(retryAfter)
    else:
        print(f"Error: {e}")
        time.sleep(10)

if __name__ == "__main__":
    # cli_menu()
    main()