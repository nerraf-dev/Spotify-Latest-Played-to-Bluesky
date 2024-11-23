import time, os, spotipy
from dotenv import load_dotenv
from utils import init_spotipy, get_track_info, get_now_playing
from atproto import Client
from bsky_utils import post_tracks, get_did_for_handle


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
    client = Client()
    client.login(os.getenv('BLUESKY_HANDLE'), os.getenv('BLUESKY_PASSWORD'))
    # Post the simulated tracks
    mention_did = get_did_for_handle(client, os.getenv('BLUESKY_MENTION_HANDLE'))
    post_tracks(listened)
    print("Test mode: Posted simulated tracks")
    return

def initialise():
    sp = init_spotipy()
    listened = []
    return (sp, None, listened)

def load_configuration():
    if not load_dotenv():
        print("""
            Error: No .env file found.
              
            To continue you will need your Spotify Developer Client ID and Client Secret.
            You can create a Spotify Developer account and create a new app to get these credentials.
            You will also need your Bluesky handle and password.
              
            Please enter the required information when prompted.
              Press Enter to continue...
            """)
        input()
        with open(".env", "w") as f:
            spotify_client_id = input("Enter Spotify Client ID: ")
            spotify_client_secret = input("Enter Spotify Client Secret: ")
            bluesky_handle = input("Enter Bluesky Handle: ")
            bluesky_password = input("Enter Bluesky Password: ")
            f.write(f"SPOTIFY_CLIENT_ID={spotify_client_id}\n")
            f.write(f"SPOTIFY_CLIENT_SECRET={spotify_client_secret}\n")
            f.write(f"SPOTIFY_REDIRECT_URI=http://localhost:1234\n")
            f.write(f"SPOTIFY_SCOPE=user-read-currently-playing\n")
            f.write(f"SPOTIFY_CACHE_PATH=.cache\n")
            f.write(f"BLUESKY_HANDLE={bluesky_handle}\n")
            f.write(f"BLUESKY_PASSWORD={bluesky_password}\n")
            print("Environment variables saved to .env file")
        return False
    return True

def main():
    if not load_configuration():
        return
    
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
    main()