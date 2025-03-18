import sys
import signal
import threading
from queue import Queue
import time
import sqlalchemy

#from server.database import Session, FeedUser, UserList, Subfeed
from server.database import FeedUser, UserList, Subfeed, SubfeedMember
from server import data_stream, config
from server.logger import logger
from server.data_filter import operations_callback, feed_users_dict, user_lists_dict, subfeeds_dict, subfeed_members_dict


def reload_on_timer(lock, stream_stop_event=None):
    #thread_session = Session()

    while True:
        if stream_stop_event and stream_stop_event.is_set():
            break

        feed_users = FeedUser.select()

        user_lists = UserList.select()
        all_list_subjects = list(set([row.subscribes_to_did for row in user_lists]))

        all_subfeed_members = list(set([row.did for row in FeedUser.select().join(SubfeedMember)]))

        subfeeds = Subfeed.select()

        with lock:
            for k, v in {row.did: row.id for row in feed_users}.items():
                feed_users_dict[k] = v

            for k, v in {row.id: row.feed_name for row in subfeeds}.items():
                subfeeds_dict[k] = v

            for k in user_lists_dict:
                if not k in all_list_subjects:
                    del user_lists_dict[k]

            for k in all_list_subjects:
                user_lists_dict[k] = ''

            for k in all_subfeed_members:
                subfeed_members_dict[k] = ''

        time.sleep(120)


def sigint_handler(*_):
    print('Stopping data stream...')
    stream_stop_event.set()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

if __name__ == '__main__':
    
    lock = threading.Lock()

    stream_stop_event = threading.Event()
    stream_thread = threading.Thread(
        target=data_stream.run, args=(config.SERVICE_DID, operations_callback, stream_stop_event,)
    )
    reload_thread = threading.Thread(target=reload_on_timer, args=(lock,stream_stop_event,))
    
    stream_thread.start()
    reload_thread.start()
