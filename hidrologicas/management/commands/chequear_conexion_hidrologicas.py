from django.core.management.base import BaseCommand
from hidrologicas.models import Hidrologica
import socket
import requests
import time

def check_port(ip, port=8080, timeout=2):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except Exception:
        return False

def check_url(ip, port=8080):
    url = f"http://{ip}:{port}/hidrosgc"
    try:
        r = requests.get(url, timeout=3)
        return r.status_code != 404
    except Exception:
        return False

class Command(BaseCommand):
    help = 'Valida el estado de conexión de las hidrológicas'

    def handle(self, *args, **options):
        hidros = Hidrologica.objects.all()
        for h in hidros:
            ip = None
            if h.tipo_conexion == 'vpn' and h.direccion_ip_vpn:
                ip = h.direccion_ip_vpn
            elif h.tipo_conexion == 'local' and h.direccion_ip_privada:
                ip = h.direccion_ip_privada
            latencia = None
            if ip:
                start = time.time()
                port_ok = check_port(str(ip))
                url_ok = check_url(str(ip))
                end = time.time()
                if port_ok and url_ok:
                    h.estado_conexion = 'online'
                    latencia = int((end - start) * 1000)
                else:
                    h.estado_conexion = 'offline'
                    latencia = None
            else:
                h.estado_conexion = 'offline'
                latencia = None
            h.latencia_ms = latencia
            h.save()
        self.stdout.write(self.style.SUCCESS('Estado de conexión actualizado.'))
