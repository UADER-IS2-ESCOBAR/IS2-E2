import unittest
from unittest.mock import patch, MagicMock
from CorporateLog import CorporateLog  # Asegúrate de que el nombre del módulo sea correcto
from boto3.dynamodb.conditions import Key
import logging

class TestCorporateLog(unittest.TestCase):

    def setUp(self):
        # Configura el logger para ver los mensajes durante las pruebas
        self.logger = logging.getLogger()
        self.previous_level = self.logger.level
        self.logger.setLevel(logging.DEBUG)

    def tearDown(self):
        # Restaura el nivel de logging original después de cada prueba
        self.logger.setLevel(self.previous_level)

    @patch('CorporateLog.boto3.resource')  # Mockear boto3 para evitar conexiones reales
    def test_post_valido(self, mock_boto_resource):
        # Configura el mock para la tabla de DynamoDB
        mock_table = MagicMock()
        mock_boto_resource.return_value.Table.return_value = mock_table

        # Crea una instancia de CorporateLog y llama al método post
        log = CorporateLog()
        log.post('67048ac6-e6e2-439f-81e8-dbce7da3e9d1', 'testMethod')

        # Verifica que put_item fue llamado en la tabla simulada
        mock_table.put_item.assert_called_once()
        # Verifica que el item tiene las claves correctas
        args, kwargs = mock_table.put_item.call_args
        self.assertIn('uuid', kwargs['Item'])
        self.assertIn('method', kwargs['Item'])
        self.assertIn('cpu', kwargs['Item'])
        self.assertIn('timestamp', kwargs['Item'])

    @patch('CorporateLog.boto3.resource')
    def test_list_con_uuid_session(self, mock_boto_resource):
        # Configura el mock para la tabla de DynamoDB
        mock_table = MagicMock()
        mock_boto_resource.return_value.Table.return_value = mock_table

        # Simula la respuesta de la consulta
        mock_table.query.return_value = {'Items': [{'uuid': '67048ac6-e6e2-439f-81e8-dbce7da3e9d1'}]}

        # Crea una instancia de CorporateLog y llama al método list con un uuid_session
        log = CorporateLog()
        items = log.list(uuid_session='67048ac6-e6e2-439f-81e8-dbce7da3e9d1')

        # Verifica que query fue llamado con el parámetro correcto
        mock_table.query.assert_called_once_with(
            KeyConditionExpression=Key('uuid').eq('67048ac6-e6e2-439f-81e8-dbce7da3e9d1')
        )
        # Verifica que la respuesta contiene el item esperado
        self.assertEqual(items, [{'uuid': '67048ac6-e6e2-439f-81e8-dbce7da3e9d1'}])

    @patch('CorporateLog.boto3.resource')
    def test_list_sin_uuid_session(self, mock_boto_resource):
        # Configura el mock para la tabla de DynamoDB
        mock_table = MagicMock()
        mock_boto_resource.return_value.Table.return_value = mock_table

        # Simula la respuesta del escaneo
        mock_table.scan.return_value = {'Items': [{'uuid': '05ff81e3-6c97-4e9b-a12d-2cefa33acdd0'}]}

        # Crea una instancia de CorporateLog y llama al método list sin un uuid_session
        log = CorporateLog()
        items = log.list()

        # Verifica que scan fue llamado
        mock_table.scan.assert_called_once()
        # Verifica que la respuesta contiene el item esperado
        self.assertEqual(items, [{'uuid': '05ff81e3-6c97-4e9b-a12d-2cefa33acdd0'}])

    def test_singleton_pattern(self):
        # Crea dos instancias de CorporateLog
        instance1 = CorporateLog()
        instance2 = CorporateLog()

        # Verifica que ambas instancias son la misma
        self.assertIs(instance1, instance2, "CorporateLog no sigue el patrón Singleton")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)  # Configura logging básico para que se vea en la consola
    unittest.main()
