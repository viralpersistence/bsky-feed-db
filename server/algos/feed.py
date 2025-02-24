from datetime import datetime
from typing import Optional

from server import config
from server.logger import logger

import sqlalchemy
from server.database import session, Post

uri = config.FEED_URI
CURSOR_EOF = 'eof'


def handler(cursor: Optional[str], limit: int) -> dict:
    logger.info("****THIS HAPPENS4*******")

    #posts = Post.select().order_by(Post.cid.desc()).order_by(Post.indexed_at.desc()).limit(limit)
    stmt = sqlalchemy.select(Post).order_by(Post.cid.desc()).order_by(Post.indexed_at.desc()).limit(limit)
    posts = session.scalars(stmt).all()

    #print(posts)

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
