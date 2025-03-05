from server.database import session, FeedUser, UserFollows
from server.logger import logger
import sqlalchemy
import requests

def add_user(requester_did: str) -> int:
    user = FeedUser(did=requester_did)
    session.add(user)
    session.commit()
    #print(user.id)

    logger.info(f'Added to feeduser: {requester_did}')

    res = requests.get(
        "https://bsky.social/xrpc/com.atproto.repo.listRecords", 
        params={
            "repo": requester_did, 
            "collection": "app.bsky.graph.follow"
        }
    )

    all_follows = []

    more_follows = True
    cursor = ''

    while more_follows:
        follows_batch = requests.get(
            "https://bsky.social/xrpc/com.atproto.repo.listRecords",
            params={
                "repo": requester_did,
                "collection": "app.bsky.graph.follow",
                "cursor": cursor
            },
        ).json()

        all_follows += [{'user_id': user.id,'follows_did': elem['value']['subject'], 'uri': elem['uri']} for elem in follows_batch['records']]

        if 'cursor' in follows_batch:
            cursor = follows_batch['cursor']
        else:
            more_follows = False

    session.execute(sqlalchemy.insert(UserFollows), all_follows)
    logger.info(f'Added to userfollows: {len(all_follows)}')

    return user.id
