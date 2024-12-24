import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from PIL import Image
from io import BytesIO

# Spotify API credentials
SPOTIFY_CLIENT_ID = "c74889fae944497c8eb4e82d26c6ec52"
SPOTIFY_CLIENT_SECRET = "84868591aaea416e8b988a5ff938a503"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"  # Redirect URI for OAuth

# Spotify API scope
scope = "user-read-currently-playing"

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope
))

def save_current_song_info():
    # Get currently playing song
    current_track = sp.current_user_playing_track()
    if current_track is None or current_track.get('is_playing') is False:
        print("No song is currently playing.")
        return

    # Extract song details
    song_title = current_track['item']['name']
    song_artist = ", ".join([artist['name'] for artist in current_track['item']['artists']])
    album_name = current_track['item']['album']['name']
    album_cover_url = current_track['item']['album']['images'][0]['url']

    # Save song details to a text file
    with open("current_song.txt", "w") as file:
        file.write(f"Title: {song_title}\n")
        file.write(f"Artist: {song_artist}\n")
        file.write(f"Album: {album_name}\n")

    # Download and save the album cover
    response = requests.get(album_cover_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save("album_cover.png")
        print("Album cover saved as album_cover.png.")
    else:
        print("Failed to download album cover.")

    print(f"Song info saved: {song_title} by {song_artist}.")

if __name__ == "__main__":
    save_current_song_info()
