# music-info
Spotify music info saver

## How to use
1. Use git clone to copy repo
2. Create "auth.env" file with 
    ```
    SPOTIFY_CLIENT_ID=***
    SPOTIFY_CLIENT_SECRET=***
    SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
    ```
    as its contents
3. Run music file using "py music.py"
4. Stop running file by typing "stop"