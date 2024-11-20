import spotipy
from spotipy.oauth2 import SpotifyOAuth
import settings

authManager = SpotifyOAuth(client_id=settings.client_id,
                                               client_secret=settings.client_secret,
                                               redirect_uri=settings.redirect_uri,
                                               scope="user-library-read user-read-playback-state user-read-recently-played",
                                               cache_path=".cache")


sp = spotipy.Spotify(auth_manager=authManager)


# artist = 'spotify:artist:75mafsNqNE1WSEVxIKuY5C'
# results = sp.artist_top_tracks(artist)

# for track in results['tracks'][:10]:
#     print('track    : ' + track['name'])
#     print('audio    : ' + track['preview_url'])
#     print('cover art: ' + track['album']['images'][0]['url'])
#     print()


current = sp.current_user_playing_track()

if current is not None:
    track_name = current['item']['name']
    artist_name = current['item']['artists'][0]['name']
    print(f"Now Playing: {track_name} by {artist_name}")
else:
    print("No track currently playing")


recent_tracks = sp.current_user_recently_played(limit=10)

for idx, item in enumerate(recent_tracks['items']):
    track = item['track']
    print(f"{idx + 1}: {track['name']} by {track['artists'][0]['name']}")