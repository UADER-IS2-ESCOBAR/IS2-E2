import json
import boto3

def list_log(uuid_cpu):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CorporateLog')

    print(f"Buscando registros con uuidCPU: {uuid_cpu}")

    
    response = table.scan(
        FilterExpression="#uuid = :uuid_cpu",
        ExpressionAttributeNames={"#uuid": "uuid"},
        ExpressionAttributeValues={":uuid_cpu": uuid_cpu}
    )
    
    items = response.get('Items', [])
    print(f"Registros encontrados: {len(items)}")
    
    return json.dumps(items, indent=4)

if __name__ == '__main__':
    uuid_cpu_a_usar = '67048ac6-e6e2-439f-81e8-dbce7da3e9d1'  
    log_json = list_log(uuid_cpu_a_usar)
    print(log_json)
