import os

from atproto import Client
from server import config

# Create a Bluesky client
bsky_client = Client("https://bsky.social")
bsky_client.login(config.HANDLE, config.PASSWORD)
