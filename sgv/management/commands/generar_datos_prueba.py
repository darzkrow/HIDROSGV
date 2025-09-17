from django.core.management.base import BaseCommand
from sgv.models import Visitante, Empleado, Oficina, Piso, Carnet, Visita
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Genera datos de prueba para visitantes, empleados, oficinas, carnets y visitas'

    def handle(self, *args, **options):
        # Crear pisos
        pisos = []
        for i in range(1, 4):
            piso, _ = Piso.objects.get_or_create(numero=str(i), nombre=f'Piso {i}')
            pisos.append(piso)
        # Crear oficinas
        oficinas = []
        for i in range(1, 6):
            oficina, _ = Oficina.objects.get_or_create(nombre=f'Oficina {100+i}', piso=random.choice(pisos))
            oficinas.append(oficina)
        # Crear carnets
        carnets = []
        for i in range(1, 11):
            carnet, _ = Carnet.objects.get_or_create(numero=f'C{i:03}', estado='disponible')
            carnets.append(carnet)
        # Crear empleados
        empleados = []
        for i in range(1, 6):
            empleado, _ = Empleado.objects.get_or_create(nombre_completo=f'Empleado {i}', identificacion=f'EMP{i:03}', activo=True)
            empleados.append(empleado)
        # Crear visitantes
        visitantes = []
        for i in range(1, 21):
            visitante, _ = Visitante.objects.get_or_create(
                nombre_completo=f'Visitante {i}',
                identificacion=f'VST{i:05}',
                telefono=f'0414{random.randint(1000000,9999999)}',
                correo=f'visitante{i}@test.com'
            )
            visitantes.append(visitante)
        # Crear visitas
        for i in range(1, 51):
            visitante = random.choice(visitantes)
            oficina = random.choice(oficinas)
            empleado = random.choice(empleados)
            carnet = random.choice(carnets)
            fecha_entrada = timezone.now() - timezone.timedelta(days=random.randint(0, 60))
            Visita.objects.create(
                visitante=visitante,
                motivo=f'Motivo visita {i}',
                oficina=oficina,
                anfitrion=empleado,
                carnet=carnet,
                fecha_entrada=fecha_entrada,
                placa_vehiculo=f'ABC{random.randint(100,999)}',
            )
        self.stdout.write(self.style.SUCCESS('Datos de prueba generados correctamente.'))
