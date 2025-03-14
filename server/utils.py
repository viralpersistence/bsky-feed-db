#from server.database import session, FeedUser, UserFollows, Post
#from server.client import bsky_client
import peewee
import requests

from server.database import db, FeedUser, UserFollows

@db.atomic()
def add_user(requester_did: str) -> int:
    feed_user = FeedUser.create(did=requester_did)

    print(feed_user)

    more_follows = True
    cursor = ''

    while more_follows:
        # TODO: limit to some high amount of follows?
        follows_batch = requests.get(
            "https://bsky.social/xrpc/com.atproto.repo.listRecords",
            params={
                "repo": requester_did,
                "collection": "app.bsky.graph.follow",
                "cursor": cursor,
                "limit": 100,
            },
        ).json()


        follows = [{'feeduser_id': feed_user.id,'follows_did': elem['value']['subject'], 'uri': elem['uri']} for elem in follows_batch['records']]

        if follows:
            #session.execute(sqlalchemy.insert(UserFollows), follows)
            #session.commit()
            #with db.atomic():
            #for post_dict in posts_to_create:
            #    Post.create(**post_dict)
            q=UserFollows.insert_many(follows)
            q.execute()

        if 'cursor' in follows_batch:
            cursor = follows_batch['cursor']
        else:
            more_follows = False

    return feed_user



def get_or_add_user(requester_did: str) -> int:
    try:
        user = add_user(requester_did)
    except peewee.IntegrityError:
        user = FeedUser.get(FeedUser.did == requester_did)
    return user

    
    




'''
def add_feed_posts(user: FeedUser) -> None:
    print(user.did)
    #pass
    data = bsky_client.get_author_feed(actor=user.did, limit=50)

    for post in data['feed']:
        posts_to_create = 

    print(dir(data['feed']))
    print(data['feed'][0])
'''


'''
def get_or_add_user(requester_did: str) -> int:
    stmt = sqlalchemy.select(FeedUser).filter(FeedUser.did == requester_did)
    rows = session.execute(stmt).fetchone()

    if rows:
        return rows[0]

    user = FeedUser(did=requester_did)
    session.add(user)
    session.commit()

    # add user follows
    #all_follows = []

    more_follows = True
    cursor = ''

    while more_follows:
        # TODO: limit to some high amount of follows?
        follows_batch = requests.get(
            "https://bsky.social/xrpc/com.atproto.repo.listRecords",
            params={
                "repo": requester_did,
                "collection": "app.bsky.graph.follow",
                "cursor": cursor,
                "limit": 100,
            },
        ).json()

        #all_follows += [{'user_id': user.id,'follows_did': elem['value']['subject'], 'uri': elem['uri']} for elem in follows_batch['records']]

        follows = [{'user_id': user.id,'follows_did': elem['value']['subject'], 'uri': elem['uri']} for elem in follows_batch['records']]

        if follows:
            session.execute(sqlalchemy.insert(UserFollows), follows)
            session.commit()

        if 'cursor' in follows_batch:
            cursor = follows_batch['cursor']
        else:
            more_follows = False

        #logger.info(f'Added to userfollows: {len(all_follows)}')

    return user
'''