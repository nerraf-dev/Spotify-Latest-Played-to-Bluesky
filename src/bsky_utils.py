from math import log
import os
from atproto import Client, client_utils

def login_bluesky():
    client = Client()
    client.login(os.getenv('BLUESKY_HANDLE'), os.getenv('BLUESKY_PASSWORD'))
    return client

def get_did_for_handle(client, handle):
    """
    Retrieve the decentralized identifier (DID) for a given handle using the provided client.

    Args:
        client: An instance of the client used to interact with the API.
        handle (str): The handle for which to resolve the DID.

    Returns:
        str: The decentralized identifier (DID) associated with the given handle.
    """
    response = client.com.atproto.identity.resolve_handle({'handle': handle})
    did = response['did']
    return did


def post_tracks(tracks):
    """
    Posts the recently listened tracks to Bluesky.
    This function logs into the Bluesky client using credentials from environment variables,
    mentions a user, and posts the titles and artists of the recently listened tracks.
    Args:
        tracks (list of dict): A list of dictionaries where each dictionary contains the following keys:
            - 'title' (str): The title of the track.
            - 'url' (str): The URL of the track.
            - 'artist' (str): The artist of the track.
    Environment Variables:
        BLUESKY_HANDLE (str): The handle for logging into Bluesky.
        BLUESKY_PASSWORD (str): The password for logging into Bluesky.
    """
    client = login_bluesky
    # userDID = get_did_for_handle(client, os.getenv('BLUESKY_MENTION_HANDLE'))
    tb = client_utils.TextBuilder()
    # tb.mention(os.getenv('BLUESKY_MENTION_HANDLE'), userDID)    
    tb.text(f" I've recently listened to:\n\n")
    for track in tracks:
        tb.link(f"{track['title']}", track['url'])
        tb.text(f" by {track['artist']}, \n")
    client.send_post(tb)

    postText = f"Recently listened to: {tracks[0]['title']} by {tracks[0]['artist']}, {tracks[1]['title']} by {tracks[1]['artist']}, {tracks[2]['title']} by {tracks[2]['artist']}"
    print(postText)