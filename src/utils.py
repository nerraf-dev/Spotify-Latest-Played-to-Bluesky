import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from atproto import Client

config = {}
# get config from credentials.json
def get_config():
    with open('src/config.json') as f:
        config = json.load(f)
    config['bluesky']['session'] = get_bsky_session(config)
    return config

def get_bsky_session(config):
    """
    Get Bluesky session
    """
    client = Client()
    session = client.login(config['bluesky']['handle'], config['bluesky']['password'])
    return session

def init_spotipy(config):
    """
    Initialize spotipy object with user credentials
    """
    # Load credentials
    # with open('credentials.json') as f:
    #     credentials = json.load(f)
    # Initialize spotipy object
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config['spotify']['client_id'],
                                                   client_secret=config['spotify']['client_secret'],
                                                   redirect_uri=config['spotify']['redirect_uri'],
                                                   scope=config['spotify']['scope'],
                                                   cache_path=config['spotify']["cache_path"]
                                                   ))
    return sp