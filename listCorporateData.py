import json
import boto3
from decimal import Decimal

def decimal_to_float(obj):
    """Convierte Decimal a float."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f'Type {type(obj)} not serializable')

def list_corporate_data():
    # Inicializa el cliente de la base de datos
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CorporateData')

    # Escanea la tabla para obtener todos los elementos
    response = table.scan()
    items = response.get('Items', [])

    # Retorna la estructura JSON
    return json.dumps(items, default=decimal_to_float, indent=4)

if __name__ == '__main__':
    corporate_data_json = list_corporate_data()
    print(corporate_data_json)
