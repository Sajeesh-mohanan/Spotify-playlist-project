import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy import SpotifyOAuth
import os
from dotenv import find_dotenv, load_dotenv

year_input = input("what year you would like to travel to in YYY-MM-DD format?\n")
URL = f"https://www.billboard.com/charts/hot-100/{year_input}/"

response = requests.get(URL)
url_txt = response.text

soup = BeautifulSoup(url_txt, "html.parser")

title_list = soup.find_all("li", class_="lrv-u-width-100p")
title_artist_list = soup.select_one("div ul li ul li span")

album = {}
for title in title_list:
    h3_tag = title.find("h3", id="title-of-a-story")
    if h3_tag is not None:
        song_title = h3_tag.get_text().strip()
        song_artist = title.find("span").get_text().strip()
        album[song_title] = song_artist


# Spotify

dotenv_path = find_dotenv()
# finding .env file

load_dotenv(dotenv_path)
# loading .env file as environmental variables

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SCRT = os.getenv("CLIENT_SCRT")


spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SCRT,
        show_dialog=True,
        cache_path="token.txt"
    )
)


USER_ID = spotify.current_user()['id']
track_uri = []
count = 0

for key in album:
    track_name = key
    track_artist = album[key]
    user_search = spotify.search(q=f"{track_name} {track_artist}", type='track')
    track_uri.append(user_search['tracks']['items'][0]['uri'])

playlist = spotify.user_playlist_create(user=USER_ID, name=f"{year_input} Billboard 100", public=False)

spotify.playlist_add_items(playlist_id=playlist['id'], items=track_uri)

