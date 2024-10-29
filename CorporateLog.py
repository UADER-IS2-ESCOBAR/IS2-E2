import boto3
import platform
from datetime import datetime
from boto3.dynamodb.conditions import Key  

class CorporateLog:
    _instance = None

    # Singleton implementation
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CorporateLog, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('CorporateLog')

    def post(self, uuid_session, method_name):
        cpu_info = platform.node()
        timestamp = datetime.now().isoformat()
        log_entry = {
            'uuid': uuid_session,
            'method': method_name,
            'cpu': cpu_info,
            'timestamp': timestamp
        }
        self.table.put_item(Item=log_entry)

    def list(self, uuid_cpu=None, uuid_session=None):
        if uuid_session:
            response = self.table.query(
                KeyConditionExpression=Key('uuid').eq(uuid_session)
            )
        else:
            response = self.table.scan()
        return response['Items']
