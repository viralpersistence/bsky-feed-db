import sys
import signal
import threading
from queue import Queue
import time
import sqlalchemy

from server.database import Session, FeedUser, UserList
from server import data_stream, config
from server.logger import logger
from server.data_filter import operations_callback, feed_users_dict, user_lists_dict

'''
class ThreadShared:

    def __init__(self, session):
        self.session = session
        stmt = sqlalchemy.select(FeedUser)
        feed_users = self.session.scalars(stmt).all()
        self.feed_users = {row.did for row in feed_users}

    def reload_from_db(self):
        stmt = sqlalchemy.select(FeedUser)
        feed_users = self.session.scalars(stmt).all()
        self.feed_users = {row.did for row in feed_users}

    def get_feed_users(self):
        return self.feed_users


def reload_on_timer(ts):
    start = time.time()
    while True:
        time.sleep(5)
        #q.put(True)
        #q = 'def'
        ts.reload_from_db()
'''

def reload_on_timer(lock, stream_stop_event=None):
    thread_session = Session()

    #start = time.time()
    while True:
        if stream_stop_event and stream_stop_event.is_set():
            #thread_session.
            break
        stmt = sqlalchemy.select(FeedUser)
        feed_users = thread_session.scalars(stmt).all()

        stmt = sqlalchemy.select(UserList)
        user_lists = thread_session.scalars(stmt).all()
        all_list_subjects = list(set([row.subscribes_to_did for row in user_lists]))
        #print(feed_users)

        with lock:
            #feed_users_dict['asdf'] = 1
            for k, v in {row.did: row.id for row in feed_users}.items():
                feed_users_dict[k] = v

            #for k in list(set([row.subscribes_to_did for row in user_lists])):
                #feed_users_dict[k] = v
            
            #user_lists_dict = all_list_subjects

            for k in user_lists_dict:
                if not k in all_list_subjects:
                    del user_lists_dict[k]

            for k in all_list_subjects:
                user_lists_dict[k] = ''
            
                

        time.sleep(60)
        #q.put(True)
        #q = 'def'
        #ts.reload_from_db()


def sigint_handler(*_):
    print('Stopping data stream...')
    stream_stop_event.set()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

if __name__ == '__main__':
    
    #q = Queue()
    #thread_session = Session()
    #ts = ThreadShared(thread_session)
    lock = threading.Lock()

    stream_stop_event = threading.Event()
    #reload_event = threading.Event()
    stream_thread = threading.Thread(
        target=data_stream.run, args=(config.SERVICE_DID, operations_callback, stream_stop_event,)
    )
    reload_thread = threading.Thread(target=reload_on_timer, args=(lock,stream_stop_event,))
    
    stream_thread.start()
    reload_thread.start()

    '''
    reload_session = Session()

    while True:
        stmt = sqlalchemy.select(FeedUser)
        feed_users = reload_session.scalars(stmt).all()
        print(feed_users)
        time.sleep(10)
    '''


