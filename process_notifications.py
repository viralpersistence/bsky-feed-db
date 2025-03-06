import time
import sqlalchemy
from atproto import models
from string import punctuation
from server.client import client
from server.database import session, Feed, FeedMember
from server.utils import get_or_add_user

# script to update feed members and settings based on notifications

punc = ''.join([elem for elem in punctuation if elem != '#'])

SUBFEED_CMDS = {
    '#IaccAddTo': 'add',
    '#IaccRemoveFrom': 'remove',
}

stmt = sqlalchemy.select(Feed)
SUBFEED_NAMES = {row.feed_name: row for row in session.scalars(stmt).all()}


SUBFEED_CMD_DICT = {''.join([cmd, subfeed_name]).lower(): (action, subfeed_name) for subfeed_name in SUBFEED_NAMES for cmd, action in SUBFEED_CMDS.items()}


SETTING_CMDS = {
    '#IaccRepliesOn'.lower(): ('replies_off', False, 'Feeds will now include replies.'),
    '#IaccRepliesOff'.lower(): ('replies_off', True, 'Feeds will no longer include replies.')
}

print(SUBFEED_CMD_DICT)


def post_contains_cmd(record):
    text_words = list(set([word.lower().strip(punc) for word in record.text.split()]))
    words_in_cmds_dict = [SUBFEED_CMD_DICT[word] for word in text_words if word in SUBFEED_CMD_DICT]

    feed_cmds = {}

    for action, subfeed_name in words_in_cmds_dict:
        if action not in feed_cmds:
            feed_cmds[action] = []
        feed_cmds[action].append(SUBFEED_NAMES[subfeed_name])

    setting_cmds = [SETTING_CMDS[word] for word in text_words if word in SETTING_CMDS]

    #print(feed_cmds)
    #print(setting_cmds)

    return feed_cmds, setting_cmds

#def post_contains_setting_cmd(record):


def main() -> None:
    #client = Client()
    #client.login('my-handle', 'my-password')

    # fetch new notifications
    while True:
        response = client.app.bsky.notification.list_notifications()
        for notification in response.notifications:
            if notification.reason == 'mention' and not notification.is_read:
            
                record = notification.record

                #if record.reply:
                root_uri = record.reply.root.uri if record.reply else notification.uri
                root_cid = record.reply.root.cid if record.reply else notification.cid
                #reply_parent = record.reply.parent.uri

                #print(notification)
                #print(reply_root)
                #print(notification.uri)
                #print(record.text)
                #print('\n')
                #continue
                #print(record.text)
                #print(type(record))

                feed_cmds, setting_cmds = post_contains_cmd(record)

                if not (feed_cmds or setting_cmds):
                    continue

                user_did = notification.author.did
                feed_user = get_or_add_user(user_did)

                messages = []

                if 'add' in feed_cmds:
                    stmt = sqlalchemy.select(FeedMember)
                    feed_members = [row for row in session.scalars(stmt).all()]

                    feed_members_to_create = []

                    for feed in feed_cmds['add']:
                        if any([fm.user_id == feed_user.id and fm.feed_id == feed.id for fm in feed_members]):
                            messages.append(f'You are already a member of {feed.feed_name}.')
                        else:
                            feed_members_to_create.append({'user_id': feed_user.id, 'feed_id': feed.id})
                            messages.append(f'Added to {feed.feed_name}.')

                    #feed_members_to_create = [{'user_id': feed_user.id, 'feed_id': feed.id} for feed in feed_cmds['add']]
                    #session.execute(sqlalchemy.insert(FeedMember), feed_members_to_create)
                    #messages += [f'Added to {feed.feed_name}' for feed in feed_cmds['add']]
                    #logger.info(f'Added to feed members: {len(feed_members_to_create)}')
                    #print(f'Added {user_did} to ')

                    if feed_members_to_create:
                        session.execute(sqlalchemy.insert(FeedMember), feed_members_to_create)

                if 'remove' in feed_cmds:
                    feeds_to_remove_from = [feed.id for feed in feed_cmds['remove']]
                    stmt = sqlalchemy.delete(FeedMember).where(sqlalchemy.and_(FeedMember.user_id == feed_user.id, FeedMember.feed_id.in_(feeds_to_remove_from)))
                    session.execute(stmt)
                    messages += [f'Removed from {feed.feed_name}' for feed in feed_cmds['remove']]

                    #logger.info(f'Deleted from feed members: {n_deletes}')

                for col_name, value, message in setting_cmds:
                    setattr(feed_user, col_name, value)
                    session.commit()
                    messages.append(message)


                reply_ref = {'uri': notification.uri, 'cid': notification.cid}
                reply_root = {'uri': root_uri, 'cid': root_cid}
                client.send_post(
                    text='\n'.join(messages),
                    #reply_to=models.AppBskyFeedPost.ReplyRef(parent=root_post_ref, root=root_post_ref),
                    reply_to=models.AppBskyFeedPost.ReplyRef(parent=reply_ref, root=reply_root),
                )

                client.app.bsky.notification.update_seen({'seen_at': client.get_current_time_iso()})



        time.sleep(10)


if __name__ == '__main__':
    main()