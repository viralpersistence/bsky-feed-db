from server.database import session, FeedUser, UserFollows
from server.logger import logger
import sqlalchemy
import requests

def get_or_add_user(requester_did: str) -> int:
    stmt = sqlalchemy.select(FeedUser).filter(FeedUser.did == requester_did)
    rows = session.execute(stmt).fetchone()

    if rows:
        return rows[0]

    user = FeedUser(did=requester_did)
    session.add(user)
    session.commit()
    #print(user.id)

    logger.info(f'Added to feeduser: {requester_did}')

    res = requests.get(
        "https://bsky.social/xrpc/com.atproto.repo.listRecords", 
        params={
            "repo": requester_did, 
            "collection": "app.bsky.graph.follow",
            "limit": 100,
        }
    )

    '''
    # add user settings

    user_setting = UserSetting(user_id=user.id, setting_name="replies_off")
    session.add(user_setting)
    session.commit()
    '''

    # add user follows
    all_follows = []

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

        all_follows += [{'user_id': user.id,'follows_did': elem['value']['subject'], 'uri': elem['uri']} for elem in follows_batch['records']]

        if 'cursor' in follows_batch:
            cursor = follows_batch['cursor']
        else:
            more_follows = False

    session.execute(sqlalchemy.insert(UserFollows), all_follows)
    logger.info(f'Added to userfollows: {len(all_follows)}')

    return user
