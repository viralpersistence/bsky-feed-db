import sys
import signal
import threading

import data_stream
import config

from logger import logger
logger.info("0")


logger.info("1")


logger.info("2")
from data_filter import operations_callback

logger.info("3")

def sigint_handler(*_):
    print('Stopping data stream...')
    stream_stop_event.set()
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)

if __name__ == '__main__':
    stream_stop_event = threading.Event()
    stream_thread = threading.Thread(
        target=data_stream.run, args=(config.SERVICE_DID, operations_callback, stream_stop_event,)
    )
    stream_thread.start()


