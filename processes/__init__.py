import os
from boto3 import resource

SQS_REGION=os.environ.get('SQS_REGION', 'us-east-1')

sqs_cli=resource('sqs', region_name=SQS_REGION)