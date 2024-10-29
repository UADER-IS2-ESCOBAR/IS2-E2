import boto3
from boto3.dynamodb.conditions import Key

class CorporateData:
    _instance = None

    # Singleton implementation
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CorporateData, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('CorporateData')

    def getData(self, uuid_session, uuid_cpu, id_sede):
        response = self.table.query(
            KeyConditionExpression=Key('id').eq(id_sede)
        )
        return response['Items'][0] if 'Items' in response and response['Items'] else {"error": "Registro no encontrado"}

    def getCUIT(self, uuid_session, uuid_cpu, id_sede):
        response = self.table.query(
            KeyConditionExpression=Key('id').eq(id_sede)
        )
        return {"CUIT": response['Items'][0]['CUIT']} if 'Items' in response and response['Items'] else {"error": "CUIT no encontrado"}

    def getSeqID(self, uuid_session, uuid_cpu, id_sede):
        response = self.table.query(
            KeyConditionExpression=Key('id').eq(id_sede)
        )
        if 'Items' in response and response['Items']:
            item = response['Items'][0]
            id_seq = item.get('seqID', 0) + 1  # Maneja si seqID no existe

            # Actualizar el seqID en la tabla
            self.table.update_item(
                Key={'id': id_sede},
                UpdateExpression="set seqID = :s",
                ExpressionAttributeValues={':s': id_seq},
                ReturnValues="UPDATED_NEW"
            )
            return {"id_sede": id_sede, "seqID": id_seq}
        else:
            return {"error": "Registro no encontrado"}

    def listCorporateData(self, uuid_session, id_sede):
        response = self.table.scan()
        return response['Items'] if 'Items' in response else {"error": "No hay datos disponibles"}
