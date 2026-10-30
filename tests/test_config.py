"""Pruebas de configuración - TP4 Gisella Henriquez (Legajo 5225).

Valida que docker/docker-compose.yml sea un YAML sintácticamente correcto
y que defina los servicios y puertos pedidos en la consigna.
"""
import os
import unittest

import yaml

RUTA_COMPOSE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "docker", "docker-compose.yml"
)


class TestDockerCompose(unittest.TestCase):

    def setUp(self):
        # yaml.safe_load lanza una excepción si el YAML tiene errores de sintaxis
        with open(RUTA_COMPOSE, encoding="utf-8") as archivo:
            self.compose = yaml.safe_load(archivo)

    def test_yaml_valido(self):
        """El archivo se interpreta como un diccionario YAML."""
        self.assertIsInstance(self.compose, dict)

    def test_servicios_definidos(self):
        """Existen los dos servicios coordinados."""
        servicios = self.compose.get("services", {})
        self.assertIn("web_server", servicios)
        self.assertIn("log_analyzer", servicios)

    def test_puertos_personalizados(self):
        """Nginx expone 8025 (8000+25) y 9025 (9000+25)."""
        puertos = self.compose["services"]["web_server"].get("ports", [])
        self.assertIn("8025:80", puertos)
        self.assertIn("9025:9025", puertos)


if __name__ == "__main__":
    unittest.main()
