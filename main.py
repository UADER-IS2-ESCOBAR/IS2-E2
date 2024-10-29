import boto3
import uuid
import platform
from datetime import datetime
from boto3.dynamodb.conditions import Key

# Clase para manejar datos corporativos
class CorporateData:
    _instance = None

    # Implementación del patrón Singleton
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CorporateData, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('CorporateData')

    def getData(self, id_sede):
        response = self.table.query(
            KeyConditionExpression=Key('id').eq(id_sede)
        )
        if 'Items' in response and response['Items']:
            return response['Items'][0]
        else:
            return {"error": "Registro no encontrado"}

    def getCUIT(self, id_sede):
        response = self.table.query(
            KeyConditionExpression=Key('id').eq(id_sede)
        )
        if 'Items' in response and response['Items']:
            return {"CUIT": response['Items'][0]['CUIT']}
        else:
            return {"error": "CUIT no encontrado"}

    def getSeqID(self, id_sede):
        response = self.table.query(
            KeyConditionExpression=Key('id').eq(id_sede)
        )
        if 'Items' in response and response['Items']:
            id_seq = response['Items'][0]['seqID'] + 1
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

    def listCorporateData(self):
        response = self.table.scan()
        return response['Items']


# Clase para manejar registros de eventos corporativos
class CorporateLog:
    _instance = None

    # Implementación del patrón Singleton
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

    def list(self, uuid_session=None):
        if uuid_session:
            response = self.table.query(
                KeyConditionExpression=Key('uuid').eq(uuid_session)
            )
        else:
            response = self.table.scan()
        return response['Items']


# Ejemplo de ejecución
if __name__ == "__main__":
    # Crear instancia de CorporateData
    corporate_data = CorporateData()
    
    # Ejemplo de uso de CorporateData
    id_sede = "001"
    data = corporate_data.getData(id_sede)
    print("Datos de CorporateData:", data)

    # Crear instancia de CorporateLog
    corporate_log = CorporateLog()

    # Definir valores de prueba
    uuid_session = str(uuid.uuid4())  # Generar un UUID único
    method_name = "testMethod"

    # Llamar al método post para registrar un evento en CorporateLog
    corporate_log.post(uuid_session, method_name)
    print(f"Evento registrado en CorporateLog para la sesión {uuid_session}.")

    # Llamar al método list para listar todos los eventos
    eventos = corporate_log.list(uuid_session=uuid_session)
    print("Eventos registrados en CorporateLog:")
    for evento in eventos:
        print(evento)
