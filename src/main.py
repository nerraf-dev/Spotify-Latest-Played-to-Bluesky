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

def main():
    load_dotenv()
    sp, currentTrack, listened = initialise()
    
    # Enable test mode
    test_mode = False
    if test_mode:
        run_test_mode()
    
    while True:
        try:
            currentTrack, duration, progress = get_now_playing(sp, currentTrack)
            # print(f"Current track: {currentTrack}")
            remainingTime = (duration - progress) / 1000    # in seconds
            # print(f"Remaining time: {remainingTime}")
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