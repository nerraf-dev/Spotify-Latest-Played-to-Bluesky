import time

from utils import get_config, init_spotipy
from spotify_utils import get_now_playing

config = {}


# def get_time_remaining(track):
#     if track:
#         return track['item']['duration_ms'] - track['progress_ms']
#     else:
#         return None

def main():

    config = get_config()
    sp = init_spotipy(config)
    currentTrack = None
    timeRemaining = 30     # seconds
    while True:
        timeRemaining, currentTrack = get_now_playing(sp, currentTrack, config)
        time.sleep(timeRemaining)


if __name__ == "__main__":
    main()