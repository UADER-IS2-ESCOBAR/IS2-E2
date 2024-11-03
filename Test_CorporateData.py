import unittest
import logging
from CorporateData import CorporateData
from uuid import uuid4

class TestCorporateData(unittest.TestCase):
    def setUp(self):
        # Configurar el logger para mostrar mensajes de depuración durante los tests
        self.logger = logging.getLogger("CorporateDataLogger")
        self.logger.setLevel(logging.DEBUG)
        self.log_handler = logging.StreamHandler()
        self.log_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(self.log_handler)
        
        # Instancia de CorporateData para pruebas
        self.corporate_data = CorporateData()
        self.uuid_session = str(uuid4())
        self.uuid_cpu = "test_cpu"
        self.id_sede_valido = "FCyT"  # ID correcto basado en tu descripción
        self.id_sede_invalido = "Inexistente"  # ID que no existe

    def tearDown(self):
        # Desactivar el logging al finalizar cada prueba
        self.logger.removeHandler(self.log_handler)
        self.logger.setLevel(logging.CRITICAL)  # Opcional, para silenciar completamente el logger

    def test_getCUIT_valido(self):
        # Test del método getCUIT con un id_sede válido
        self.logger.debug("Ejecutando test_getCUIT_valido")
        result = self.corporate_data.getCUIT(self.uuid_session, self.uuid_cpu, self.id_sede_valido)
        self.logger.debug("Resultado de getCUIT válido: %s", result)
        self.assertIn("CUIT", result, "CUIT no encontrado en la base de datos")

    def test_getCUIT_invalido(self):
        # Test del método getCUIT con un id_sede inválido
        self.logger.debug("Ejecutando test_getCUIT_invalido")
        result = self.corporate_data.getCUIT(self.uuid_session, self.uuid_cpu, self.id_sede_invalido)
        self.logger.debug("Resultado de getCUIT inválido: %s", result)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "CUIT no encontrado")

    def test_getCUIT_argumento_faltante(self):
        # Test del método getCUIT sin argumento id_sede
        self.logger.debug("Ejecutando test_getCUIT_argumento_faltante")
        result = self.corporate_data.getCUIT(self.uuid_session, self.uuid_cpu, "")
        self.logger.debug("Resultado de getCUIT con argumento vacío: %s", result)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "CUIT no encontrado")

    def test_getSeqID_valido(self):
        # Test del método getSeqID con un id_sede válido
        self.logger.debug("Ejecutando test_getSeqID_valido")
        result = self.corporate_data.getSeqID(self.uuid_session, self.uuid_cpu, self.id_sede_valido)
        self.logger.debug("Resultado de getSeqID válido: %s", result)
        self.assertIn("seqID", result, "seqID no encontrado en la base de datos")

    def test_getSeqID_invalido(self):
        # Test del método getSeqID con un id_sede inválido
        self.logger.debug("Ejecutando test_getSeqID_invalido")
        result = self.corporate_data.getSeqID(self.uuid_session, self.uuid_cpu, self.id_sede_invalido)
        self.logger.debug("Resultado de getSeqID inválido: %s", result)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Registro no encontrado")

    def test_getSeqID_argumento_faltante(self):
        # Test del método getSeqID con argumento faltante para id_sede
        self.logger.debug("Ejecutando test_getSeqID_argumento_faltante")
        result = self.corporate_data.getSeqID(self.uuid_session, self.uuid_cpu, "")
        self.logger.debug("Resultado de getSeqID con argumento faltante: %s", result)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "id_sede no puede estar vacío")

    def test_singleton_pattern(self):
        # Test para comprobar que CorporateData sigue el patrón Singleton
        self.logger.debug("Ejecutando test_singleton_pattern")
        instance1 = CorporateData()
        instance2 = CorporateData()
        self.logger.debug("Verificando que ambas instancias sean iguales")
        
        # Verifica que ambas instancias son la misma
        self.assertIs(instance1, instance2, "CorporateData no sigue el patrón Singleton")

if __name__ == "__main__":
    unittest.main()
