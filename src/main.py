import time, spotipy, os
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

def cli_menu():
    if not load_configuration():
        return
    print("""
        Welcome to the Spotify Bluesky Integration!
        This script will listen for tracks you play on Spotify and post them to Bluesky.
          
        """)
    while True:
        # print("""
        # 1. Check Spotify Details
        # 2. Check Bluesky Details
        # 3. Update Details
        # 4. Run Test Mode
        # 5. Start Listening for Tracks
        # 6. Exit
        # """)
        print("""

        3. Update Details

        5. Start Listening for Tracks
        6. Exit
        """)
        choice = input("Enter your choice: ")
        # if choice == '1':
        #     check_spotify_details()
        # elif choice == '2':
        #     check_bluesky_details()
        if choice == '3':
            update_details()
        # elif choice == '4':
        #     run_test_mode()
        elif choice == '5':
            main()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

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
    
    print(f"Listening for tracks...")
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