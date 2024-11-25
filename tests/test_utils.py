import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils import init_spotipy, update_details
from spotipy.exceptions import SpotifyException

class TestUtils(unittest.TestCase):

    @patch('utils.SpotifyOAuth')
    def test_init_spotipy_missing_client_id(self, mock_spotify_oauth):
        with patch.dict(os.environ, {'SPOTIPY_CLIENT_ID': ''}):
            with self.assertRaises(SpotifyException):
                init_spotipy()

    @patch('utils.SpotifyOAuth')
    def test_init_spotipy_invalid_credentials(self, mock_spotify_oauth):
        mock_spotify_oauth.side_effect = SpotifyException(400, -1, "Invalid credentials")
        with self.assertRaises(SpotifyException):
            init_spotipy()

    @patch('builtins.input', side_effect=['client_id', 'client_secret', 'handle', 'password'])
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_update_details(self, mock_open, mock_input):
        update_details()
        mock_open.assert_called_once_with('.env', 'w')
        handle = mock_open()
        handle.write.assert_any_call('SPOTIFY_CLIENT_ID=client_id\n')
        handle.write.assert_any_call('SPOTIFY_CLIENT_SECRET=client_secret\n')
        handle.write.assert_any_call('BLUESKY_HANDLE=handle\n')
        handle.write.assert_any_call('BLUESKY_PASSWORD=password\n')

if __name__ == '__main__':
    unittest.main()