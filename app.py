import falcon
import time
from threading import Thread, active_count

from routes.Ping import Ping
from routes.Producer import SQSProducer as Producer
from constants import QUEUE_NAME

from processes.sqs_puller import sqs_consumer
from processes.worker_pool import process_tasks

print('Active threads before starting daemon are...')
print(active_count())
print('starting thread as daemon...')
t=Thread(target=sqs_consumer, args=(QUEUE_NAME, '', ''), daemon=True)
t.start()
print('thread running as daemon')
print('Active threads after starting daemon are...')
print(active_count())
api = falcon.API()
api.add_route('/ping', Ping())
api.add_route('/api/v1/message', Producer())

if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()