import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from bsky_utils import login_bluesky, get_did_for_handle
from atproto.exceptions import UnauthorizedError

class TestBskyUtils(unittest.TestCase):

    @patch('bsky_utils.Client')
    def test_login_bluesky_invalid_credentials(self, mock_client):
        mock_client.return_value.login.side_effect = UnauthorizedError("Invalid credentials")
        client = login_bluesky()
        self.assertIsNone(client)

    @patch('bsky_utils.Client')
    def test_get_did_for_handle(self, mock_client):
        mock_client.return_value.com.atproto.identity.resolve_handle.return_value = {'did': 'did:example:123'}
        client = mock_client()
        did = get_did_for_handle(client, 'handle')
        self.assertEqual(did, 'did:example:123')

if __name__ == '__main__':
    unittest.main()