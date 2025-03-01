import os

from atproto import Client
from server import config

# Create a Bluesky client
client = Client("https://bsky.social")
client.login(config.HANDLE, config.PASSWORD)
