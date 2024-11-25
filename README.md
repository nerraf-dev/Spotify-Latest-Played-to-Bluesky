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


## Usage

1. Run the application:

    ```bash
    python src/main.py
    ```

2. The application will start listening for tracks on Spotify and post them to Bluesky.

