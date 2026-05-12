import requests
from datetime import datetime
from feedgen.feed import FeedGenerator

USERNAME = "renova_competition"

URL = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={USERNAME}"

headers = {
    "User-Agent": "Mozilla/5.0",
    "x-ig-app-id": "936619743392459"
}

response = requests.get(URL, headers=headers)

data = response.json()

user = data["data"]["user"]

posts = user["edge_owner_to_timeline_media"]["edges"]

fg = FeedGenerator()

fg.id(f"https://www.instagram.com/{USERNAME}/")

fg.title(f"{USERNAME} Instagram Feed")

fg.author({
    "name": USERNAME
})

fg.link(
    href="https://leclerctroppoforte.github.io/RENOVA-COMPETITION-FEED/feed.xml",
    rel="self"
)

fg.link(
    href=f"https://www.instagram.com/{USERNAME}/",
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

    content = f"""
    <p>{caption}</p>

    <img src="{image_url}" width="100%" />

    <p>
      <a href="{post_url}">
        Apri su Instagram
      </a>
    </p>
    """

    fe = fg.add_entry()

    fe.id(post_url)

    fe.title(
        caption[:60] if caption else "Instagram Post"
    )

    fe.link(href=post_url)

    fe.updated(updated)

    fe.summary(caption)

    fe.content(content, type="html")

fg.atom_file("feed.xml")

print("Feed aggiornato!")
