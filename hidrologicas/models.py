from django.db import models

class Gerente(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"

class Hidrologica(models.Model):
    latencia_ms = models.PositiveIntegerField("Latencia (ms)", null=True, blank=True)
    estado_conexion = models.CharField("Estado de conexión", max_length=10, choices=[('online','Online'),('offline','Offline')], default='offline')
    datacenter_hidroven = models.BooleanField("DataCenter - Hidroven", default=False)
    nombre_delhidrologica = models.CharField("Nombre de la hidrológica", max_length=150)
    acronimo = models.CharField("Acrónimo", max_length=20)
    rif = models.CharField("RIF", max_length=15, unique=True)
    ciclo_lectura = models.CharField("Ciclo de lectura", max_length=2)
    logo = models.ImageField(upload_to='hidrologicas_logos/', blank=True, null=True)
    direccion_ip_publica = models.GenericIPAddressField("IP pública", protocol='both', unpack_ipv4=True, null=True, blank=True)
    direccion_ip_privada = models.GenericIPAddressField("IP privada", protocol='both', unpack_ipv4=True, null=True, blank=True)
    direccion_ip_vpn = models.GenericIPAddressField("IP VPN", protocol='both', unpack_ipv4=True, null=True, blank=True)
    tipo_conexion = models.CharField("Tipo de conexión", max_length=10, choices=[('local','Local'),('vpn','VPN')])
    url = models.URLField("URL", max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_delhidrologica} ({self.acronimo})"
