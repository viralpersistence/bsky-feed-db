import datetime
from dateutil import parser

from collections import defaultdict

from atproto import models

from server import config
from server.logger import logger
from server.client import client
import sqlalchemy
#from database import conn#db, Post
from server.database import session, Post, FeedUser, UserFollows
from server.search_terms import post_contains_any, post_contains_link_term

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
feed_users = {row.did: row.id for row in session.scalars(stmt).all()}

def operations_callback(ops: defaultdict) -> None:
    # Here we can filter, process, run ML classification, etc.
    # After our feed alg we can save posts into our DB
    # Also, we should process deleted posts to remove them from our DB and keep it in sync

    # for example, let's create our custom feed that will contain all posts that contains alf related text


    #stmt = sqlalchemy.select(FeedUser)
    #feed_users = {row.did: row.id for row in session.scalars(stmt).all()}
    #self.feed_users = {row.did for row in feed_users}

    logger.info(ops[models.ids.AppBskyGraphFollow])

    
    userfollows_to_create = []
    for created_follow in ops[models.ids.AppBskyGraphFollow]['created']:
        #print(myobj)
        if created_follow['author'] == 'did:plc:ptqbnzqvblvezfga4zpqocu4':
            print('here')
            #print(feed_users)

        
        author_uses_feed = created_follow['author'] in feed_users
        if not author_uses_feed:
            continue

        post_dict = {
            'user_id': feed_users[created_follow['author']],
            'uri': created_follow['uri'],
            'follows_did': created_follow['record'].subject,
        }

        print('this happens0')

        userfollows_to_create.append(post_dict)
        

    if userfollows_to_create:
        session.execute(sqlalchemy.insert(UserFollows), userfollows_to_create)
        logger.info(f'Added to userfollows: {len(userfollows_to_create)}')

    userfollows_to_delete = ops[models.ids.AppBskyGraphFollow]['deleted']
    if userfollows_to_delete:
        userfollows_uris_to_delete = [userfollow['uri'] for userfollow in userfollows_to_delete]

        stmt = sqlalchemy.delete(UserFollows).where(UserFollows.uri.in_(userfollows_uris_to_delete))
        session.execute(stmt)

        logger.info(f'Deleted from userfollows: {len(userfollows_uris_to_delete)}')
    

    #at://did:plc:ptqbnzqvblvezfga4zpqocu4/app.bsky.graph.follow/3ljlykzbclg2k
    #at://did:plc:ptqbnzqvblvezfga4zpqocu4/app.bsky.graph.follow/3ljlystq6uj22


    

    '''
    unfollows = ops[models.ids.AppBskyGraphFollow]['deleted']
    if unfollows:
        follow_uris_to_delete = [record['uri'] for record in unfollows]
        stmt = sqlalchemy.delete(UserFollows).where(UserFollows.uri.in_(follow_uris_to_delete))
        session.execute(stmt)

        logger.info(f'Deleted from userfollows: {len(follow_uris_to_delete)}')
    '''

    posts_to_create = []
    for created_post in ops[models.ids.AppBskyFeedPost]['created']:
        author = created_post['author']
        record = created_post['record']

        post_with_images = isinstance(record.embed, models.AppBskyEmbedImages.Main)
        post_with_video = isinstance(record.embed, models.AppBskyEmbedVideo.Main)
        post_with_external = isinstance(record.embed, models.AppBskyEmbedExternal.Main)
        inlined_text = record.text.replace('\n', ' ')

        #if post_with_external:
        #    print(record.embed)

        # print all texts just as demo that data stream works
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

        if post_with_external and not should_appear:
            should_appear = post_contains_link_term(record)

        #if post_contains_any(record):
        if should_appear:
            reply_root = reply_parent = None
            if record.reply:
                reply_root = record.reply.root.uri
                reply_parent = record.reply.parent.uri

                #print(record.reply)
                #post = models.app.bsky.feed.getPosts({'uris': [reply_root, reply_parent]})
                #print(posts)
                
                print(inlined_text)
                res = client.get_posts(uris=[reply_root, reply_parent])
                thread_dids = [thread_post.author.did for thread_post in res.posts]
                print(thread_dids)


            post_dict = {
                'uri': created_post['uri'],
                'cid': created_post['cid'],
                'reply_parent': reply_parent,
                'reply_root': reply_root,
                'did': author,
                'discoverable': discoverable,
                'has_link': post_with_external,
                'indexed_at': parser.parse(record.created_at),
            }
            posts_to_create.append(post_dict)

            if discoverable:
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

        logger.info(f'Deleted from feed: {len(post_uris_to_delete)}')

    if posts_to_create:
        session.execute(sqlalchemy.insert(Post), posts_to_create)
        logger.info(f'Added to feed: {len(posts_to_create)}')
