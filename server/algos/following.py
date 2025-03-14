from datetime import datetime
from typing import Optional
#import sqlalchemy
#from sqlalchemy import and_

from server import config
from server.logger import logger
#from server.database import session, Post, UserFollows#, User, Follows
from server.database import Post, UserFollows
from server.utils import get_or_add_user

uri = config.FOLLOWING_FEED_URI
CURSOR_EOF = 'eof'

'''
def get_follows(requester_did: str) -> list:
    res = client.get_follows(requester_did)
    follows_cursor = res.cursor
    all_followed_dids = [elem['did'] for elem in res.follows]

    while follows_cursor is not None:
        res = client.get_follows(requester_did, cursor=follows_cursor)
        follows_cursor = res.cursor
        all_followed_dids += [elem['did'] for elem in res.follows]

    return all_followed_dids
'''


def handler(cursor: Optional[str], limit: int, requester_did: str) -> dict:

    
    user = get_or_add_user(requester_did)

    '''
    if user.replies_off:
        where_stmt = and_(
            Post.link_only == 0,
            Post.userlist_only == 0,
            Post.subfeed_only == None,
            UserFollows.user_id == user.id,
            Post.reply_parent == None,
            Post.reply_root == None
        )
    else:
        where_stmt = and_(
            Post.link_only == 0,
            Post.userlist_only == 0,
            Post.subfeed_only == None,
            UserFollows.user_id == user.id
        )

    stmt = sqlalchemy.select(Post).join(UserFollows, Post.did == UserFollows.follows_did).where(where_stmt).order_by(Post.indexed_at.desc()).limit(limit)
    posts = session.scalars(stmt).all()
    '''

    if user.replies_off:
        where_stmt = (
            (Post.link_only == 0) &
            (Post.userlist_only == 0) &
            (Post.subfeed_only == None) &
            (UserFollows.feeduser_id == user.id) &
            (Post.reply_parent == None) &
            (Post.reply_root == None)
        )
    else:
        where_stmt = (
            (Post.link_only == 0) &
            (Post.userlist_only == 0) &
            (Post.subfeed_only == None) &
            (UserFollows.feeduser_id == user.id)
        )

    posts = Post.select().join(UserFollows, on=(Post.did == UserFollows.follows_did)).where(where_stmt).order_by(Post.cid.desc()).order_by(Post.indexed_at.desc())


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
