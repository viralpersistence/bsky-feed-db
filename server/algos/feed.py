from datetime import datetime
from typing import Optional

from server import config
from server.logger import logger
from server.client import client

import sqlalchemy
from server.database import session, Post, User, Follows

uri = config.FEED_URI
CURSOR_EOF = 'eof'

'''
def add_user(requester_did: str):
    stmt = sqlalchemy.insert(User).values(did=requester_did)
    session.execute(stmt)
    logger.info(f'Added user {requester_did}')

    all_followed_dids = []
    res = client.get_follows(requester_did)
    follows_cursor = res.cursor

    while follows_cursor is not None:
        all_followed_dids += [elem['did'] for elem in res.follows]
        res = client.get_follows(requester_did, cursor=follows_cursor)
        follows_cursor = res.cursor

    follows_to_create = [{'did': requester_did, 'follows_did': did} for did in all_followed_dids]
    session.execute(sqlalchemy.insert(Follows), follows_to_create)
    logger.info(f'Added to follows: {len(follows_to_create)}')
'''

def get_follows(requester_did: str) -> list:
    all_followed_dids = []
    res = client.get_follows(requester_did)
    follows_cursor = res.cursor

    while follows_cursor is not None:
        all_followed_dids += [elem['did'] for elem in res.follows]
        res = client.get_follows(requester_did, cursor=follows_cursor)
        follows_cursor = res.cursor

    return all_followed_dids


def handler(cursor: Optional[str], limit: int, requester_did: str) -> dict:

    #stmt = sqlalchemy.select(Post).order_by(Post.cid.desc()).order_by(Post.indexed_at.desc()).limit(limit)
    #posts = session.scalars(stmt).all()

    '''
    stmt = sqlalchemy.select(Follows).filter(Follows.did == requester_did)
    rows = session.execute(stmt).fetchone()

    if not rows:
        add_user(requester_did)
    '''

    all_followed_dids = get_follows(requester_did)
    logger.info(f"Retrieved {len(all_followed_dids)} for user {requester_did}")

    stmt = sqlalchemy.select(Post).where(Post.did.in_(all_followed_dids)).order_by(Post.cid.desc()).order_by(Post.indexed_at.desc()).limit(limit)
    posts = session.scalars(stmt).all()


    if cursor:
        if cursor == CURSOR_EOF:
            return {
                'cursor': CURSOR_EOF,
                'feed': []
            }
        cursor_parts = cursor.split('::')
        if len(cursor_parts) != 2:
            raise ValueError('Malformed cursor')

        indexed_at, cid = cursor_parts
        indexed_at = datetime.fromtimestamp(int(indexed_at) / 1000)
        #posts = posts.where(((Post.indexed_at == indexed_at) & (Post.cid < cid)) | (Post.indexed_at < indexed_at))
        posts = [post for post in posts if (post.indexed_at == indexed_at and post.cid < cid) or post.indexed_at < indexed_at]

    feed = [{'post': post.uri} for post in posts]

    cursor = CURSOR_EOF
    last_post = posts[-1] if posts else None
    if last_post:
        cursor = f'{int(last_post.indexed_at.timestamp() * 1000)}::{last_post.cid}'

    return {
        'cursor': cursor,
        'feed': feed
    }


if __name__ == '__main__':
    handler(limit=10)
