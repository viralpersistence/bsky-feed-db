import sys
import signal
import threading
from queue import Queue
import time

from server import data_stream, config
from server.logger import logger
from server.data_filter import operations_callback


def sigint_handler(*_):
    print('Stopping data stream...')
    stream_stop_event.set()
    sys.exit(0)

def reload_timer(q):
    start = time.time()
    while True:
        time.sleep(5)
        q.put(True)
        


signal.signal(signal.SIGINT, sigint_handler)

if __name__ == '__main__':
    q = Queue()

    stream_stop_event = threading.Event()
    reload_event = threading.Event()
    stream_thread = threading.Thread(
        target=data_stream.run, args=(config.SERVICE_DID, operations_callback, q, stream_stop_event,)
    )
    timer_thread = threading.Thread(target=reload_timer, args=(q,))
    stream_thread.start()
    timer_thread.start()


