import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from PIL import Image
from io import BytesIO
import time
import threading

# Spotify API credentials
SPOTIFY_CLIENT_ID = "your_client_id"
SPOTIFY_CLIENT_SECRET = "your_client_secret"
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

    while running:
        try:
            # Get currently playing song
            current_track = sp.current_user_playing_track()
            if current_track is None or current_track.get('is_playing') is False:
                print("No song is currently playing.")
                time.sleep(1)  # Wait for 1 second before checking again
                continue

            # Extract song details
            song_id = current_track['item']['id']  # Unique song identifier
            if song_id == last_song_id:
                # Skip updating if the song hasn't changed
                time.sleep(1)
                continue

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
                print(f"Updated: {song_title} by {song_artist}. Album cover saved.")
            else:
                print("Failed to download album cover.")

            # Update the last song ID
            last_song_id = song_id

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
