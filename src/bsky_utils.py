import time
from atproto import Client
from atproto_client.models.app.bsky.embed.external import External
import requests
from bs4 import BeautifulSoup

def fetch_embed_url_card(access_token: str, url: str) -> dict:
    # the required fields for every embed card
    card = {
        "uri": url,
        "title": "",
        "description": "",
    }

    # fetch the HTML
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # parse out the "og:title" and "og:description" HTML meta tags
    title_tag = soup.find("meta", property="og:title")
    if title_tag:
        card["title"] = title_tag["content"]
    description_tag = soup.find("meta", property="og:description")
    if description_tag:
        card["description"] = description_tag["content"]

    # if there is an "og:image" HTML meta tag, fetch and upload that image
    image_tag = soup.find("meta", property="og:image")
    if image_tag:
        img_url = image_tag["content"]
        # naively turn a "relative" URL (just a path) into a full URL, if needed
        if "://" not in img_url:
            img_url = url + img_url
        resp = requests.get(img_url)
        resp.raise_for_status()

        pds_url = url  # Define the pds_url variable with the appropriate URL
        blob_resp = requests.post(
            pds_url + "/xrpc/com.atproto.repo.uploadBlob",
            headers={
                "Content-Type": "image/jpeg",  # Adjust the MIME type as needed
                "Authorization": "Bearer " + access_token,
            },
            data=resp.content,
        )
        blob_resp.raise_for_status()
        card["thumb"] = blob_resp.json()["blob"]

    return {
        "$type": "app.bsky.embed.external",
        "external": card,
    }



def post_now_playing(config, nowPlaying):
    """
    Post the current track to the Bluesky client
    """
    client = Client()
    session = client.login(config['bluesky']['handle'], config['bluesky']['password'])
    postText = f"Now Playing: {nowPlaying['title']} by {nowPlaying['artist']}"
    url = nowPlaying['url']

    # Fetch the embed card for the URL
    embed = fetch_embed_url_card(config['bluesky']['session'], url)

    client.send_post(text=postText, embed=embed)
    print(postText)