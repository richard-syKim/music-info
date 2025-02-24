from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import spotipy
import os

# Get the absolute path to the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

print(script_dir)

# Load .env file using absolute path
dotenv_path = os.path.join(script_dir, "auth.env")
load_dotenv(dotenv_path)

print(dotenv_path)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-currently-playing"
))

print(f"Client ID: {SPOTIFY_CLIENT_ID}")
print(f"Client Secret: {SPOTIFY_CLIENT_SECRET}")
print(f"Redirect URI: {SPOTIFY_REDIRECT_URI}")

print("Authentication successful!")