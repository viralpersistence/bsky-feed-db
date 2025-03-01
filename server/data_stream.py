import logging
from collections import defaultdict

from atproto import AtUri, CAR, firehose_models, FirehoseSubscribeReposClient, models, parse_subscribe_repos_message
from atproto.exceptions import FirehoseError

#from database import conn#SubscriptionState
from server.logger import logger

import sqlalchemy
from server.database import session, SubscriptionState

_INTERESTED_RECORDS = {
    models.AppBskyFeedLike: models.ids.AppBskyFeedLike,
    models.AppBskyFeedPost: models.ids.AppBskyFeedPost,
    models.AppBskyGraphFollow: models.ids.AppBskyGraphFollow,
}


def _get_ops_by_type(commit: models.ComAtprotoSyncSubscribeRepos.Commit) -> defaultdict:
    operation_by_type = defaultdict(lambda: {'created': [], 'deleted': []})

    car = CAR.from_bytes(commit.blocks)
    for op in commit.ops:
        if op.action == 'update':
            # we are not interested in updates
            continue

        uri = AtUri.from_str(f'at://{commit.repo}/{op.path}')

        if op.action == 'create':
            if not op.cid:
                continue

            create_info = {'uri': str(uri), 'cid': str(op.cid), 'author': commit.repo}

            record_raw_data = car.blocks.get(op.cid)
            if not record_raw_data:
                continue

            record = models.get_or_create(record_raw_data, strict=False)
            if record is None:  # unknown record (out of bsky lexicon)
                continue

            for record_type, record_nsid in _INTERESTED_RECORDS.items():
                if uri.collection == record_nsid and models.is_record_type(record, record_type):
                    operation_by_type[record_nsid]['created'].append({'record': record, **create_info})
                    break

        if op.action == 'delete':
            operation_by_type[uri.collection]['deleted'].append({'uri': str(uri)})

    return operation_by_type

def run(name, operations_callback, q, stream_stop_event=None):
    while stream_stop_event is None or not stream_stop_event.is_set():
        try:
            _run(name, operations_callback, q, stream_stop_event)
        except FirehoseError as e:
            if logger.level == logging.DEBUG:
                raise e
            logger.error(f'Firehose error: {e}. Reconnecting to the firehose.')


def _run(name, operations_callback, q, stream_stop_event=None):
    print('...')
    #state = SubscriptionState.get_or_none(SubscriptionState.service == name)
    #rows = db.execute("""SELECT cursor FROM subscriptionstate WHERE service = (?);""", (name)).fetchall()
    #print(rows)

    stmt = sqlalchemy.select(SubscriptionState).filter(SubscriptionState.service == name)
    rows = session.execute(stmt).fetchone()
    print(rows)
    #print(rows[0].cursor)

    params = None
    #if state:
    if rows:
        #params = models.ComAtprotoSyncSubscribeRepos.Params(cursor=state.cursor)
        #print(dir(rows[0]))
        params = models.ComAtprotoSyncSubscribeRepos.Params(cursor=rows[0].cursor)

    client = FirehoseSubscribeReposClient(params)

    #if not state:
    #    SubscriptionState.create(service=name, cursor=0)

    if not rows:
        stmt = sqlalchemy.insert(SubscriptionState).values(service=name, cursor=0)
        session.execute(stmt)
        #db.execute("""INSERT INTO subscriptionstate (service, cursor) VALUES (?,?);""", (name, 0))

    def on_message_handler(message: firehose_models.MessageFrame) -> None:

        if q.empty():
            reload = False
        else:
            reload = q.get()


        # stop on next message if requested
        if stream_stop_event and stream_stop_event.is_set():
            client.stop()
            return

        commit = parse_subscribe_repos_message(message)
        if not isinstance(commit, models.ComAtprotoSyncSubscribeRepos.Commit):
            return

        # update stored state every ~1k events
        if commit.seq % 1000 == 0:  # lower value could lead to performance issues
            logger.debug(f'Updated cursor for {name} to {commit.seq}')
            client.update_params(models.ComAtprotoSyncSubscribeRepos.Params(cursor=commit.seq))
            
            #SubscriptionState.update(cursor=commit.seq).where(SubscriptionState.service == name).execute()
            #db.execute("""UPDATE subscriptionstate SET cursor=(?) WHERE name=(?);""", (commit.seq, name))
            stmt = sqlalchemy.update(SubscriptionState).where(SubscriptionState.service == name).values(cursor=commit.seq)
            session.execute(stmt)


        if not commit.blocks:
            return

        operations_callback(_get_ops_by_type(commit), reload=reload)

    client.start(on_message_handler)