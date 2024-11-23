import os
from atproto import Client, client_utils

def post_now_playing(nowPlaying):
    """
    Post the current track to the Bluesky client
    """
    client = Client()
    client.login(os.getenv('BLUESKY_HANDLE'), os.getenv('BLUESKY_PASSWORD'))
    userDID = get_did_for_handle(client, os.getenv('BLUESKY_MENTION_HANDLE'))
    tb = client_utils.TextBuilder()

    tb.mention(os.getenv('BLUESKY_MENTION_HANDLE'), userDID)
    tb.text(f" is currently listening to  \n\n")
    tb.link(f"{nowPlaying['title']}", nowPlaying['url'])
    tb.text(f" by {nowPlaying['artist']}")
    client.send_post(tb)

    # postText = f"Now Playing: {nowPlaying['title']} by {nowPlaying['artist']}"
    # url = nowPlaying['url']
    # print(postText)


def get_did_for_handle(client, handle):
    """
    Get the DID of a user by their handle
    """
    response = client.com.atproto.identity.resolve_handle({'handle': handle})
    did = response['did']
    return did


def post_tracks(tracks):
    """
    Post the current track to the Bluesky client
    """
    client = Client()
    client.login(os.getenv('BLUESKY_HANDLE'), os.getenv('BLUESKY_PASSWORD'))
    userDID = get_did_for_handle(client, os.getenv('BLUESKY_MENTION_HANDLE'))
    tb = client_utils.TextBuilder()
    tb.mention(os.getenv('BLUESKY_MENTION_HANDLE'), userDID)
    tb.text(f" recently listened to: : \n\n")
    tb.link(f"{tracks[0]['title']} ", tracks[0]['url'])
    tb.text(f"by {tracks[0]['artist']}, \n")
    tb.link(f"{tracks[1]['title']} ", tracks[1]['url'])
    tb.text(f"by {tracks[1]['artist']}, \n")
    tb.link(f"{tracks[2]['title']} ", tracks[2]['url'])
    tb.text(f"by {tracks[2]['artist']}\n")
    
    client.send_post(tb)

    postText = f"Recently listened to: {tracks[0]['title']} by {tracks[0]['artist']}, {tracks[1]['title']} by {tracks[1]['artist']}, {tracks[2]['title']} by {tracks[2]['artist']}"
    print(postText)