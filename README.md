# Spotify-Playing-Now

Spotify-Playing-Now is a Python application that posts the tracks you are currently listening to on Spotify to Bluesky. It can also post the last three tracks you listened to if you have listened to at least 75% of each track.

## Features

- Posts the currently playing track on Spotify to Bluesky.
- Posts the last three tracks you listened to on Spotify to Bluesky.
- Configurable via environment variables.
- Test mode to simulate posting tracks without actually listening to them.

## Requirements

- Python 3.7+
- Spotify Developer Account
- Bluesky Account

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/Spotify-Playing-Now.git
    cd Spotify-Playing-Now
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file from the example:

    ```bash
    cp .env.example .env
    ```

5. Fill in your own values in the `.env` file:

    ```env
    SPOTIFY_CLIENT_ID=your_spotify_client_id
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIFY_REDIRECT_URI=http://localhost:1234
    SPOTIFY_SCOPE=user-library-read user-read-playback-state user-read-recently-played
    SPOTIFY_CACHE_PATH=.cache
    BLUESKY_HANDLE=your_bluesky_handle
    BLUESKY_PASSWORD=your_bluesky_password
    BLUESKY_MENTION_HANDLE=@handle-to-mention
    ```

## Usage

1. Run the application:

    ```bash
    python src/main.py
    ```

2. The application will start listening for tracks on Spotify and post them to Bluesky.

## Test Mode

To quickly test the functionality without listening to tracks, you can enable test mode. In `src/main.py`, set `test_mode` to `True`:

```python
    # Enable test mode
    test_mode = True
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## 
License
This project is licensed under the MIT License. See the LICENSE file for details.


