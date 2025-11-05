import streamlit as st
from google import genai
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth


#Spotify Auth
CLIENT_ID = "68b20273e5014771a020054bbfd16e4b"
CLIENT_SECRET = "5caf2b74eedd4d01a57eb381898ed52f"


#Chrome Header
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

#playlist id
playlist_id = "https://open.spotify.com/playlist/5g8HbxMydMbjbafbtOWRt6?si=bdf566c3ef6f4cf5"

#Establish Connection with Spotify
authentication = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="www.thimphutechpark.com")
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-public",
        redirect_uri="https://www.billboard.com/charts/hot-100/2025-09-13/",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="kalden")
)


#Client Initialize for Gemini API
client = genai.Client(api_key="AIzaSyC0TLFI2LTF3wl_uI0257w4CIsOO_Zq8o8")

#Setting up StreamLit Page
st.set_page_config(page_title="Spotify Playlist Creator", page_icon="🎧", layout="centered")
st.title("Spotify Playlist Creator with AI")
st.text("Enter Prompt Below")
user_input = st.text_input(label="Prompt")
if st.button("Process"):
    result = user_input

    #Feed user response as prompt
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="I am creating a playlist and based on the description Just give me a list of 15 songs separated by a ;. I Don't want any extra response Description: "+ result
    )
    #Response Formatting
    song_list = [response.text.split(";")]
    df = pd.DataFrame(song_list)
    df_transposed = df.transpose()
    st.write(df_transposed)


    #Remove All songs from the playlist
    # tracks_to_remove = []
    # remove_uri = sp.playlist_items(playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=('track', 'episode'))
    # print(remove_uri[0:2])
    # sp.playlist_remove_all_occurrences_of_items(playlist_id, tracks_to_remove, snapshot_id=None)


    # Add songs to the playlist
    song_uri = []
    for song in song_list[0]:
        result = sp.search(q=f"track:{song}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uri.append(uri)
        except IndexError:
            st.write(f"{song} doesn't exist in Spotify. Skipped.")

    # Now configuring spotify
    sp.playlist_replace_items(playlist_id=playlist_id, items=song_uri)




