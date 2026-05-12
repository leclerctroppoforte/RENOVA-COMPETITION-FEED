import requests
from feedgen.feed import FeedGenerator
from datetime import datetime
import json

USERNAME = "renova_competition"

url = f"https://www.instagram.com/{USERNAME}/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(url, headers=headers).text

start = html.find('window._sharedData = ')
end = html.find(';</script>', start)

json_data = html[start + 21:end]
data = json.loads(json_data)

posts = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]

fg = FeedGenerator()

fg.id(url)
fg.title(f"{USERNAME} Instagram Feed")
fg.author({'name': USERNAME})
fg.link(href=url, rel='alternate')
fg.link(href='https://YOUR_USERNAME.github.io/renova-instagram-feed/feed.xml', rel='self')
fg.language('it')

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
    <![CDATA[
        <p>{caption}</p>
        <img src="{image_url}" width="100%" />
        <p><a href="{post_url}">Apri su Instagram</a></p>
    ]]>
    """

    fe = fg.add_entry()

    fe.id(post_url)
    fe.title(caption[:60] if caption else "Instagram Post")
    fe.link(href=post_url)
    fe.updated(updated)
    fe.summary(caption)
    fe.content(content, type='html')

fg.atom_file('feed.xml')

print("Feed aggiornato!")
