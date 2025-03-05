import sys
import signal
import threading
from queue import Queue
import time
import sqlalchemy

from server.database import Session, FeedUser, UserFollows
from server import data_stream, config
from server.logger import logger
from server.data_filter import operations_callback

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


def sigint_handler(*_):
    print('Stopping data stream...')
    stream_stop_event.set()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

if __name__ == '__main__':
    
    #q = Queue()
    #thread_session = Session()
    #ts = ThreadShared(thread_session)

    stream_stop_event = threading.Event()
    #reload_event = threading.Event()
    stream_thread = threading.Thread(
        target=data_stream.run, args=(config.SERVICE_DID, operations_callback, stream_stop_event,)
    )
    #timer_thread = threading.Thread(target=reload_on_timer, args=(ts,))
    stream_thread.start()
    #timer_thread.start()


