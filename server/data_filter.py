import datetime
from dateutil import parser

from collections import defaultdict

from atproto import models

from server import config
from server.logger import logger
import sqlalchemy
#from database import conn#db, Post
from server.database import session, Post, FeedUser, UserFollows, UserList, Subfeed#, FeedMember
from server.search_terms import post_contains_any, post_contains_link_term, post_contains_subfeed_term
from server.utils import get_or_add_user

import time

# Open the connection to SQLite Cloud
#conn = sqlitecloud.connect(config.SQLITE_CONN_STRING)
#db = conn.cursor()


def is_archive_post(record: 'models.AppBskyFeedPost.Record') -> bool:
    # Sometimes users will import old posts from Twitter/X which con flood a feed with
    # old posts. Unfortunately, the only way to test for this is to look an old
    # created_at date. However, there are other reasons why a post might have an old
    # date, such as firehose or firehose consumer outages. It is up to you, the feed
    # creator to weigh the pros and cons, amd and optionally include this function in
    # your filter conditions, and adjust the threshold to your liking.
    #
    # See https://github.com/MarshalX/bluesky-feed-generator/pull/21

    archived_threshold = datetime.timedelta(days=1)
    created_at = datetime.datetime.fromisoformat(record.created_at)
    now = datetime.datetime.now(datetime.UTC)

    return now - created_at > archived_threshold


def should_ignore_post(record: 'models.AppBskyFeedPost.Record') -> bool:
    if config.IGNORE_ARCHIVED_POSTS and is_archive_post(record):
        logger.debug(f'Ignoring archived post: {record.uri}')
        return True

    if config.IGNORE_REPLY_POSTS and record.reply:
        logger.debug(f'Ignoring reply post: {record.uri}')
        return True

    return False


stmt = sqlalchemy.select(FeedUser)
feed_users_dict = {row.did: row.id for row in session.scalars(stmt).all()}

stmt = sqlalchemy.select(Subfeed)
subfeeds_dict = {row.id: row.feed_name for row in session.scalars(stmt).all()}

'''
stmt = sqlalchemy.select(FeedMember)
feed_members_dict = {}

for row in session.scalars(stmt).all():
    did = {v: k for k, v in feed_users_dict.items()}[row.user_id]

    if did not in feed_members_dict:
        feed_members_dict[did] = []

    feed_members_dict[did].append(row.feed_id)
'''

stmt = sqlalchemy.select(UserList)
user_lists_dict = {row.subscribes_to_did: '' for row in session.scalars(stmt).all()}


def operations_callback(ops: defaultdict) -> None:
    # Here we can filter, process, run ML classification, etc.
    # After our feed alg we can save posts into our DB
    # Also, we should process deleted posts to remove them from our DB and keep it in sync

    #print(subfeeds_dict)

    
    userfollows_to_create = []
    for created_follow in ops[models.ids.AppBskyGraphFollow]['created']:
        
        author_uses_feed = created_follow['author'] in feed_users_dict
        if not author_uses_feed:
            continue

        post_dict = {
            'user_id': feed_users_dict[created_follow['author']],
            'uri': created_follow['uri'],
            'follows_did': created_follow['record'].subject,
        }

        userfollows_to_create.append(post_dict)
        

    if userfollows_to_create:
        session.execute(sqlalchemy.insert(UserFollows), userfollows_to_create)
        session.commit()
        logger.info(f'Added to userfollows: {len(userfollows_to_create)}')

    userfollows_to_delete = ops[models.ids.AppBskyGraphFollow]['deleted']
    if userfollows_to_delete:
        userfollows_uris_to_delete = [userfollow['uri'] for userfollow in userfollows_to_delete]

        stmt = sqlalchemy.delete(UserFollows).where(UserFollows.uri.in_(userfollows_uris_to_delete))
        session.execute(stmt)
        session.commit()

        logger.info(f'Deleted from userfollows: {len(userfollows_uris_to_delete)}')
    

    posts_to_create = []
    for created_post in ops[models.ids.AppBskyFeedPost]['created']:
        author = created_post['author']
        record = created_post['record']

        if type(record) == int:
            print('????????????')
            print(created_post)

        post_with_images = isinstance(record.embed, models.AppBskyEmbedImages.Main)
        post_with_video = isinstance(record.embed, models.AppBskyEmbedVideo.Main)
        post_with_external = isinstance(record.embed, models.AppBskyEmbedExternal.Main)
        inlined_text = record.text.replace('\n', ' ')

        '''
        logger.debug(
            f'NEW POST '
            f'[CREATED_AT={record.created_at}]'
            f'[AUTHOR={author}]'
            f'[WITH_IMAGE={post_with_images}]'
            f'[WITH_VIDEO={post_with_video}]'
            f': {inlined_text}'
        )
        '''

        if should_ignore_post(record):
            continue
        

        should_appear, discoverable = post_contains_any(record)

        link_only = False

        if post_with_external and not should_appear:
            if post_contains_link_term(record):
                should_appear = True
                link_only = True
        #userlist_only = not should_appear

        

        #if author in feed_members_dict:
        #    for feed_id in feed_members_dict[author]:
        #        feed_name = feeds_dict[feed_id]
        #        if post_contains_subfeed_term(record, feed_name)

        subfeed_only = None

        if not should_appear:
            for subfeed_id, subfeed_name in subfeeds_dict.items():
                if (not record.reply) and post_contains_subfeed_term(record, subfeed_name):
                    should_appear = True
                    subfeed_only = subfeed_id


        if should_appear:
            userlist_only = False
        elif author in user_lists_dict:
            should_appear = True
            userlist_only = True

        if should_appear:
            reply_root = reply_parent = None
            if record.reply:
                reply_root = record.reply.root.uri
                reply_parent = record.reply.parent.uri

            post_dict = {
                'uri': created_post['uri'],
                'cid': created_post['cid'],
                'reply_parent': reply_parent,
                'reply_root': reply_root,
                'did': author,
                'discoverable': discoverable,
                'has_link': post_with_external,
                'link_only': link_only,
                'userlist_only': userlist_only,
                'subfeed_only': subfeed_only,
                'indexed_at': parser.parse(record.created_at),
            }
            posts_to_create.append(post_dict)

            #if discoverable:
            logger.info(
                f'NEW POST '
                f'[CREATED_AT={record.created_at}]'
                f'[AUTHOR={author}]'
                f'[WITH_IMAGE={post_with_images}]'
                f'[WITH_VIDEO={post_with_video}]'
                f': {inlined_text}'
            )

    posts_to_delete = ops[models.ids.AppBskyFeedPost]['deleted']
    if posts_to_delete:
        post_uris_to_delete = [post['uri'] for post in posts_to_delete]

        stmt = sqlalchemy.delete(Post).where(Post.uri.in_(post_uris_to_delete))
        session.execute(stmt)
        session.commit()

        logger.info(f'Deleted from feed: {len(post_uris_to_delete)}')

    if posts_to_create:
        session.execute(sqlalchemy.insert(Post), posts_to_create)
        logger.info(f'Added to feed: {len(posts_to_create)}')
        session.commit()
