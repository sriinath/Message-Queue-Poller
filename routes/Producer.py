import os
import json
import time
from falcon import HTTPInternalServerError, HTTP_200, HTTPUnprocessableEntity
from json.decoder import JSONDecodeError
from botocore.exceptions import ParamValidationError

from processes import sqs_cli
from constants import QUEUE_NAME, RETRY_MESSAGE_LIMIT
from routes.Base import Base

class SQSProducer(Base):
    def on_post(self, req, resp):
        try:
            print('in post')
            req_body=json.load(req.bounded_stream)
            if req_body is not None:
                try:
                    queue = sqs_cli.get_queue_by_name(QueueName=QUEUE_NAME)
                    if type(req_body) == 'list' and len(req_body):
                        entries=req_body
                        print(entries)
                        response=queue.send_messages(Entries=entries)
                        failed_entries=response.get('Failed')
                        print(failed_entries)
                    else:
                        message=req_body.get('message', '')
                        attributes=req_body.get('attributes', {})
                        if message:
                            response=queue.send_message(MessageBody=message, MessageAttributes=attributes)
                            print(response)
                        else:
                            raise Exception(412, 'Request body is mandatory to process this request')
                except ParamValidationError as SQSValidationError:
                    print('Exception occured while triying to push into sqs', SQSValidationError)
                    raise Exception(422, SQSValidationError)
                except Exception as SQSError:
                    print('Exception occured while triying to push into sqs', SQSError)
                    raise Exception(500, SQSError)
            else:
                raise Exception(412, 'Request body is mandatory to process this request')
            resp.body=json.dumps({
                'status': 'Success',
                'message': 'Successfully added to the queue'
            })
            resp.status=HTTP_200
        except JSONDecodeError as err:
            print('Request body received', req.bounded_stream.read())
            print('Error while processing request', err)
            raise HTTPUnprocessableEntity(description='Error while processing request')
        except Exception as e:
            print('Exception occured while pushing message into sqs', e)
            error_code, message = e.args
            self.send_HTTP_error(error_code=error_code, message=message)
