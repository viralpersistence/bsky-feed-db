from datetime import datetime
from typing import Optional

from server import config
from server.logger import logger
from server.utils import get_or_add_user

import sqlalchemy
from sqlalchemy import or_
from server.database import session, Post#, User, Follows

uri = config.LINKS_FEED_URI
CURSOR_EOF = 'eof'


def get_follows(requester_did: str) -> list:
    res = client.get_follows(requester_did)
    follows_cursor = res.cursor
    all_followed_dids = [elem['did'] for elem in res.follows]

    while follows_cursor is not None:
        res = client.get_follows(requester_did, cursor=follows_cursor)
        follows_cursor = res.cursor
        all_followed_dids += [elem['did'] for elem in res.follows]

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

    #all_followed_dids = get_follows(requester_did)
    #logger.info(f"Retrieved {len(all_followed_dids)} for user {requester_did}")

    #stmt = sqlalchemy.select(Post).where(Post.discoverable and Post.reply_root is None and Post.reply_parent is None and not Post.did.in_(all_followed_dids)).order_by(Post.cid.desc()).order_by(Post.indexed_at.desc()).limit(limit)
    #stmt = sqlalchemy.select(Post).filter(Post.has_link).where(or_(Post.did.in_(all_followed_dids), Post.discoverable == 1)).order_by(Post.indexed_at.desc()).limit(limit)
    #posts = session.scalars(stmt).all()

    user = get_or_add_user(requester_did)

    stmt = sqlalchemy.select(UserFollows).filter(UserFollows.user_id == user_id)
    userfollows_dids = [uf.follows_did for uf in session.scalars(stmt).all()]

    if user.replies_off:
        where_stmt = or_(
            Post.did.in_(userfollows_dids),
            Post.discoverable == 1,
            Post.userlist_only == 0,
            Post.reply_parent == None,
            Post.reply_root == None,
        )

    else:
        where_stmt = or_(
            Post.did.in_(userfollows_dids),
            Post.discoverable == 1,
            Post.userlist_only == 0,
        )

    stmt = sqlalchemy.select(Post).filter(Post.has_link == 1).where(where_stmt).order_by(Post.indexed_at.desc()).limit(limit)
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
