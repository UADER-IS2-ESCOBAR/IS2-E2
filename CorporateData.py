import boto3
from boto3.dynamodb.conditions import Key

class CorporateData:
    _instance = None

    # Singleton 
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
        # Verificar si id_sede está vacío
        if not id_sede:
            return {"error": "CUIT no encontrado"}

        # Realizar la consulta en DynamoDB
        response = self.table.query(
            KeyConditionExpression=Key('id').eq(id_sede)
        )

        # Verificar si hay resultados
        if 'Items' in response and response['Items']:
            return {"CUIT": response['Items'][0]['CUIT']}
        else:
            return {"error": "CUIT no encontrado"}

    def getSeqID(self, uuid_session, uuid_cpu, id_sede):
        # Verificar si el id_sede está vacío
        if not id_sede:
            return {"error": "id_sede no puede estar vacío"}

        # Realizar la consulta en la tabla de DynamoDB
        response = self.table.query(
            KeyConditionExpression=Key('id').eq(id_sede)
        )

        # Verificar si hay elementos en la respuesta
        if 'Items' in response and response['Items']:
            item = response['Items'][0]
            id_seq = item.get('seqID', 0) + 1  

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

