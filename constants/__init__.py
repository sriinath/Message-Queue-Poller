import os

QUEUE_NAME=os.environ.get('QUEUE_NAME', '')
CONSUME_MESSAGE_DELAY=5
RETRY_MESSAGE_LIMIT=3
MAX_MESSAGE_DELAY=60
MAX_MESSAGE=10
MAX_THREAD_LIMIT=16