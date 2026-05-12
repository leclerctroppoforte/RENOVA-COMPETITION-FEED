import requests

feed_url = "https://rsshub.app/instagram/user/renova_competition"

response = requests.get(feed_url)

with open("feed.xml", "wb") as file:
    file.write(response.content)

print("feed.xml aggiornato!")
