import requests
import re
import json

from datetime import datetime
from feedgen.feed import FeedGenerator

USERNAME = "renova_competition"

url = f"https://www.instagram.com/{USERNAME}/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

html = response.text

match = re.search(r'window\._sharedData = (.*?);</script>', html)

if not match:
    raise Exception("Instagram data non trovati")

data = json.loads(match.group(1))

posts = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]

fg = FeedGenerator()

fg.id(url)

fg.title(f"{USERNAME} Instagram Feed")

fg.author({
    "name": USERNAME
})

fg.link(
    href="https://leclerctroppoforte.github.io/RENOVA-COMPETITION-FEED/feed.xml",
    rel="self"
)

fg.link(
    href=url,
    rel="alternate"
)

fg.language("it")

for post in posts[:12]:

    node = post["node"]

    shortcode = node["shortcode"]

    post_url = f"https://www.instagram.com/p/{shortcode}/"

    caption = ""

    edges = node["edge_media_to_caption"]["edges"]

    if edges:
        caption = edges[0]["node"]["text"]

    image_url = node["display_url"]

    updated = datetime.utcfromtimestamp(
        node["taken_at_timestamp"]
    )

    fe = fg.add_entry()

    fe.id(post_url)

    fe.title(
        caption[:60] if caption else "Instagram Post"
    )

    fe.link(href=post_url)

    fe.updated(updated)

    fe.summary(caption)

    fe.content(
        f"""
        <img src="{image_url}" />

        <p>{caption}</p>

        <p>
            <a href="{post_url}">
                Apri su Instagram
            </a>
        </p>
        """,
        type="html"
    )

fg.atom_file("feed.xml")

print("feed.xml generato!")
