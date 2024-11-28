from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "d35acb3f4dce46e88c925a2ed1e99e53"
CLIENT_SECRET = "ad7bd656fe5440b094a68461c456286b"
URL_REDIRECT = "http://example.com"

# ---------------------------------- Get Billboard Top 100 Songs & Artists -------------------------------------------

date = input("Which year do you want to travel to? Type the date in this format: YYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(URL)
billboard_site = response.text

soup = BeautifulSoup(billboard_site, "html.parser")

songs = soup.findAll(name="h3", class_="lrv-u-font-size-16", id="title-of-a-story")
song_titles = [title.text.strip() for title in songs]

artists = soup.findAll(name="span", class_="lrv-u-font-size-14@mobile-max")
artist_list = [name.text.strip() for name in artists]

# ------------------------------------------- Spotify Request --------------------------------------------------------

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
for song, artist in zip(song_titles, artist_list):
    result = sp.search(q=f"track:{song}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
        pass

playlist_id = sp.user_playlist_create(user_id, "Billboard Hot 100", public=False)['id']

sp.playlist_add_items(playlist_id, song_uris)
print("Playlist complete!")