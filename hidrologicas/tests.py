from django.test import TestCase
from .models import Hidrologica

class HidrologicaModelTest(TestCase):
    def setUp(self):
        self.hidro = Hidrologica.objects.create(
            nombre_delhidrologica="Hidrocapital",
            acronimo="HC",
            rif="J-12345678-9",
            ciclo_lectura="Mensual",
            url="https://hidrocapital.gob.ve",
            direccion_ip_publica="200.1.1.1",
            direccion_ip_privada="10.0.0.1",
            tipo_conexion="vpn",
            datacenter_hidroven=True,
            latencia_ms=50,
            estado_conexion="online"
        )

    def test_str(self):
        self.assertEqual(str(self.hidro), "Hidrocapital (HC)")

    def test_fields(self):
        self.assertEqual(self.hidro.acronimo, "HC")
        self.assertEqual(self.hidro.rif, "J-12345678-9")
        self.assertEqual(self.hidro.ciclo_lectura, "Mensual")
        self.assertEqual(self.hidro.url, "https://hidrocapital.gob.ve")
        self.assertEqual(self.hidro.direccion_ip_publica, "200.1.1.1")
        self.assertEqual(self.hidro.direccion_ip_privada, "10.0.0.1")
        self.assertEqual(self.hidro.tipo_conexion, "vpn")
        self.assertTrue(self.hidro.datacenter_hidroven)
        self.assertEqual(self.hidro.latencia_ms, 50)
        self.assertEqual(self.hidro.estado_conexion, "online")

    def test_update_estado_conexion(self):
        self.hidro.estado_conexion = "offline"
        self.hidro.save()
        self.assertEqual(Hidrologica.objects.get(pk=self.hidro.pk).estado_conexion, "offline")

    def test_update_latencia(self):
        self.hidro.latencia_ms = 120
        self.hidro.save()
        self.assertEqual(Hidrologica.objects.get(pk=self.hidro.pk).latencia_ms, 120)
