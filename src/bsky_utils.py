import time
from atproto import Client, client_utils
import requests
from bs4 import BeautifulSoup



def post_now_playing(client, nowPlaying):
    """
    Post the current track to the Bluesky client
    """
    # client = Client()
    # client.login(config['bluesky']['handle'], config['bluesky']['password'])

    tb = client_utils.TextBuilder()
    tb.text = f"Now Playing: {nowPlaying['title']} by {nowPlaying['artist']}"
    tb.url = nowPlaying['url']
    client.send_post()

    postText = f"Now Playing: {nowPlaying['title']} by {nowPlaying['artist']}"
    url = nowPlaying['url']
    print(postText)



    # client.send_post(text=postText)
    print(postText)