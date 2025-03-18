#from server.database import session, FeedUser, UserFollows, Post
#from server.client import bsky_client
import peewee
import requests
import time

from server.database import db, FeedUser, UserFollows, UserList

def get_uf_handles(feed_user):
    userfollows = UserFollows.select().where(UserFollows.feeduser_id == feed_user.id)
    usersubscribes = UserList.select().where(UserList.feeduser_id == feed_user.id)
    
    max_profiles = 25

    for idx in range(0, len(userfollows), max_profiles):
        sl = userfollows[idx:min(len(userfollows), idx + max_profiles)]
        sl_dids = [elem.follows_did for elem in sl]

        #print(len(sl_dids))

        actor_batch = requests.get(
            "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles",
            params={
                "actors": sl_dids
            }
        ).json()

        #for elem in actor_batch['profiles']:
        #    if 'displayName' not in elem:
        #        print(elem)


        uf_actors = [{'did': actor['did'], 'handle': actor['handle'], 'disp_name': actor['displayName']} for actor in actor_batch['profiles'] if 'handle' in actor and 'displayName' in actor]
        if not uf_actors:
            continue

        #print(actor_batch['profiles'])

        case_stmt = peewee.Case(UserFollows.follows_did, [(actor['did'], actor['handle']) for actor in uf_actors])
        query = UserFollows.update(follows_handle=case_stmt).where(UserFollows.follows_did.in_([actor['did'] for actor in uf_actors]))
        query.execute()

        case_stmt = peewee.Case(UserFollows.follows_did, [(actor['did'], actor['disp_name']) for actor in uf_actors])
        query = UserFollows.update(follows_disp_name=case_stmt).where(UserFollows.follows_did.in_([actor['did'] for actor in uf_actors]))
        query.execute()

        #time.sleep(10)


    for idx in range(0, len(usersubscribes), max_profiles):
        sl = usersubscribes[idx:min(len(usersubscribes), idx + max_profiles)]
        sl_dids = [elem.subscribes_did for elem in sl]

        actor_batch = requests.get(
            "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles",
            params={
                "actors": sl_dids
            }
        ).json()


        uf_actors = [{'did': actor['did'], 'handle': actor['handle'], 'disp_name': actor['displayName']} for actor in actor_batch['profiles'] if 'handle' in actor and 'displayName' in actor]
        if not uf_actors:
            continue

        case_stmt = peewee.Case(UserList.subscribes_did, [(actor['did'], actor['handle']) for actor in uf_actors])
        query = UserList.update(subscribes_handle=case_stmt).where(UserList.subscribes_did.in_([actor['did'] for actor in uf_actors]))
        query.execute()

        case_stmt = peewee.Case(UserList.subscribes_did, [(actor['did'], actor['disp_name']) for actor in uf_actors])
        query = UserList.update(subscribes_disp_name=case_stmt).where(UserList.subscribes_did.in_([actor['did'] for actor in uf_actors]))
        query.execute()



@db.atomic()
def add_user(requester_did):
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



def get_or_add_user(requester_did):
    #if db.is_closed():
    #    db.connect()
        
    try:
        user = add_user(requester_did)
    except peewee.IntegrityError:
        user = FeedUser.get(FeedUser.did == requester_did)
    return user

'''
def get_or_add_from_script(requester_did):
    if db.is_closed():
        db.connect()

    return get_or_add_user(requester_did)
'''
    
    




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