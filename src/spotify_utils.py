from utils import init_spotipy
from bsky_utils import post_now_playing

# def get_now_playing(sp, currentTrack, client):
#     track = sp.current_user_playing_track()     # Get track info
#     if track and track['item']:
#         duration = track['item']['duration_ms'] # in milliseconds
#         timeRemaining = max(0, duration - track['progress_ms'])/1000 # in seconds
#         nowPlaying = get_track_info(track)
#         if nowPlaying != currentTrack:
#             post_now_playing(client, nowPlaying)
#             # print(now_playing)
#             currentTrack = nowPlaying
#         else:
#             print("No change in track")
#     else:
#         print("No track currently playing")
#         timeRemaining = 30
#     return (timeRemaining, currentTrack)

# def get_track_info(track):
#     if track and track['item']:
#         return {
#             "title": track['item']['name'],
#             "artist": track['item']['artists'][0]['name'],
#             "url": track['item']['external_urls']['spotify']
#         }
#     else:
#         return None

def get_last_10_tracks(sp):
    recent_tracks = sp.current_user_recently_played(limit=10)

    for idx, item in enumerate(recent_tracks['items']):
        track = item['track']
        print(f"{idx + 1}: {track['name']} by {track['artists'][0]['name']}")