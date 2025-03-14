from datetime import datetime
from typing import Optional

from server import config
from server.logger import logger
from server.utils import get_or_add_user

import sqlalchemy
from sqlalchemy import or_, and_
from server.database import Post, Subfeed, SubfeedMember#, User, Follows

uri = config.MUTUALAID_FEED_URI
CURSOR_EOF = 'eof'

feed_name = 'mutualaid'


#stmt = sqlalchemy.select(Subfeed)
#subfeed_id = [row.id for row in session.scalars(stmt).all() if row.feed_name == feed_name][0]

subfeed = Subfeed.get(Subfeed.feed_name == feed_name)
subfeed_id = subfeed.id

logger.info("what the fuck")
logger.info(subfeed_id)


def handler(cursor: Optional[str], limit: int, requester_did: str) -> dict:
    logger.info("seriously what the fuck is going on")
    #return {
    #    'cursor': CURSOR_EOF,
    #    'feed': []
    #}

    user = get_or_add_user(requester_did)
    #userfollows_dids = [uf.follows_did for uf in user.follows]

    logger.info("what the fuck is going on")
    logger.info(subfeed_id)

    #member_ids = SubfeedMember.select().where(SubfeedMember.subfeed_id == subfeed_id)
    member_ids = [member.feeduser.did for member in subfeed.members]

    logger.info(member_ids)

    if user.replies_off:
        where_stmt = (
            (Post.userlist_only == 0) &
            (Post.link_only == 0) &
            (Post.did.in_(member_ids))
            (Post.subfeed_only.in_([None, subfeed_id])) &
            (Post.reply_parent == None) &
            (Post.reply_root == None)
        )

    else:
        where_stmt = (
            (Post.userlist_only == 0) &
            (Post.link_only == 0) &
            (Post.did.in_(member_ids)) &
            (Post.subfeed_only.in_([None, subfeed_id]))
        )

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

        where_stmt = (where_stmt & ( ( (Post.indexed_at == indexed_at) & (Post.cid < cid)  ) | (Post.indexed_at < indexed_at) ) )

    posts = Post.select().where(where_stmt).order_by(Post.cid.desc()).order_by(Post.indexed_at.desc()).limit(limit)

    '''
    stmt = sqlalchemy.select(SubfeedMember).filter(SubfeedMember.subfeed_id == subfeed_id)
    member_ids = [fm.user_id for fm in session.scalars(stmt).all()]


    #stmt = sqlalchemy.select(UserFollows).filter(UserFollows.user_id == user.id)
    #userfollows_dids = [uf.follows_did for uf in session.scalars(stmt).all()]

    if user.replies_off:
        where_stmt = and_(
            Post.userlist_only == 0,
            Post.link_only == 0,
            Post.did.in_(member_ids),
            Post.subfeed_only.in_([None, subfeed_id]),
            Post.reply_parent == None,
            Post.reply_root == None,
        )

    else:
        where_stmt = and_(
            Post.userlist_only == 0,
            Post.link_only == 0,
            Post.did.in_(member_ids),
            Post.subfeed_only.in_([None, subfeed_id])
        )

    stmt = sqlalchemy.select(Post).where(where_stmt).order_by(Post.indexed_at.desc()).limit(limit)
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
    '''

    feed = [{'post': post.uri} for post in posts]

    cursor = CURSOR_EOF
    last_post = posts[-1] if posts else None
    if last_post:
        cursor = f'{int(last_post.indexed_at.timestamp() * 1000)}::{last_post.cid}'

    return {
        'cursor': cursor,
        'feed': feed
    }
