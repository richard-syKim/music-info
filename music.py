import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from PIL import Image
from io import BytesIO
import time
import threading
from dotenv import load_dotenv
import os

# Get the absolute path to the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

print(script_dir)

# Load .env file using absolute path
dotenv_path = os.path.join(script_dir, "auth.env")
load_dotenv(dotenv_path)

print(dotenv_path)

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Spotify API scope
scope = "user-read-currently-playing"

cache_path = os.path.join(script_dir, ".cache")

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope,
    cache_path=cache_path  # Store cache in script's directory
))

# Flag to control the loop
running = True


def stop_listener():
    """Listen for the user to type 'stop' to end the loop."""
    global running
    while running:
        user_input = input("Type 'stop' to end: ").strip().lower()
        if user_input == "stop":
            running = False
            print("Stopping the program...")


def save_current_song_info():
    """Save the current song info to a file and refresh every second."""
    global running
    last_song_id = None  # Track the last played song to avoid unnecessary updates
    set_bool = False
    default_path = os.path.join(script_dir, "default.png")
    album_path = os.path.join(script_dir, "album_cover.png")
    song_text_path = os.path.join(script_dir, "current_song.txt")
    try:
        default_image = Image.open(default_path)
        default_image.save(album_path)
        print("Default image set.")
    except FileNotFoundError:
        print("default.png not found. Make sure it's in the same directory.")
    with open(song_text_path, "w", encoding="utf-8") as file:
        file.write(f"")

    while running:
        try:
            # Get currently playing song
            current_track = sp.current_user_playing_track()
            if current_track is None or current_track.get('is_playing') is False:
                print("No song is currently playing.")
                if set_bool:
                    try:
                        default_image = Image.open(default_path)
                        default_image.save(album_path)
                        print("Default image set.")
                    except FileNotFoundError:
                        print("default.png not found. Make sure it's in the same directory.")
                    with open(song_text_path, "w", encoding="utf-8") as file:
                        file.write(f"")
                    set_bool = False
                time.sleep(1)  # Wait for 1 second before checking again
                continue

            # Extract song details
            song_id = current_track['item']['id']  # Unique song identifier
            if song_id == last_song_id and set_bool:
                # Skip updating if the song hasn't changed
                time.sleep(1)
                continue
            
            song_title = current_track['item']['name']
            song_artist = ", ".join([artist['name'] for artist in current_track['item']['artists']])
            album_name = current_track['item']['album']['name']
            album_cover_url = current_track['item']['album']['images'][0]['url']

            # Save song details to a text file
            with open(song_text_path, "w", encoding="utf-8") as file:
                if len(song_title) > 30:
                    song_title = song_title[:30] + ".."
                if len(song_artist) > 20:
                    song_artist = song_artist[:20] + ".."
                file.write(f"{song_artist} - {song_title}")
                # file.write(f"Album: {album_name}\n")

            # Download and save the album cover
            response = requests.get(album_cover_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                image.save(album_path)
                print(f"Updated: {song_title} by {song_artist}. Album cover saved.")
            else:
                print("Failed to download album cover.")

            # Update the last song ID
            last_song_id = song_id
            set_bool = True

        except Exception as e:
            print(f"Error: {e}")

        # Wait for 1 second before refreshing
        time.sleep(1)


if __name__ == "__main__":
    # Start the stop listener in a separate thread
    listener_thread = threading.Thread(target=stop_listener, daemon=True)
    listener_thread.start()

    # Run the main function to save current song info
    save_current_song_info()

    # Wait for the listener thread to finish
    listener_thread.join()
    print("Program ended.")
