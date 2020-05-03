import time

from processes import sqs_cli
from processes.worker_pool import process_tasks
from constants import MAX_MESSAGE_DELAY, CONSUME_MESSAGE_DELAY, MAX_MESSAGE

MESSAGE_DELAY=CONSUME_MESSAGE_DELAY

def sqs_consumer(queue_name, callback_url, authorization):
    global MESSAGE_DELAY 
    if queue_name:
        queue=sqs_cli.get_queue_by_name(QueueName=queue_name)
        while True:
            print('consuming....')
            message=queue.receive_messages()
            message_len=len(message)
            if message_len:
                MESSAGE_DELAY=CONSUME_MESSAGE_DELAY
                for data in message:
                    process_tasks(process_messages, data, callback_url, authorization)
            else:
                if (MESSAGE_DELAY + CONSUME_MESSAGE_DELAY) >= MAX_MESSAGE_DELAY:
                    MESSAGE_DELAY=MAX_MESSAGE_DELAY
                else:
                    MESSAGE_DELAY+=CONSUME_MESSAGE_DELAY
            time.sleep(MESSAGE_DELAY)
    else:
        raise Exception('queue_name and callback_url is mandatory')

def process_messages(message, callback_url, authorization):
    if message.body:
        print(message.body)
    message.delete()