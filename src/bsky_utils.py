import time
from atproto import Client, client_utils
import requests
from bs4 import BeautifulSoup



def post_now_playing(client, nowPlaying):
    """
    Post the current track to the Bluesky client
    """

    tb = client_utils.TextBuilder()
    tb.text = f"Now Playing: {nowPlaying['title']} by {nowPlaying['artist']}"
    tb.url = nowPlaying['url']
    client.send_post()

    postText = f"Now Playing: {nowPlaying['title']} by {nowPlaying['artist']}"
    url = nowPlaying['url']
    print(postText)



    # client.send_post(text=postText)
    print(postText)


def get_did_for_handle(client, handle):
    """
    Get the DID of a user by their handle
    """
    # client = Client()
    # client.login(username, password)

    response = client.com.atproto.identity.resolve_handle({'handle': handle})
    did = response['did']
    return did


def post_tracks(client, tracks):
    """
    Post the current track to the Bluesky client
    """
    userDID = get_did_for_handle(client, 'whats-playing-bot.bsky.social')
    tb = client_utils.TextBuilder()
    tb.mention('@compscisi.bsky.social', userDID)
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