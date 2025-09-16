from django.core.management.base import BaseCommand
from hidrologicas.models import Gerente, Hidrologica

class Command(BaseCommand):
    # Eliminar hidrológicas y gerentes previos
    Hidrologica.objects.filter(nombre_delhidrologica__in=['Hidrosuroeste','Hidrocapital']).delete()
    Gerente.objects.filter(cedula__in=['10000001','10000002']).delete()
    help = 'Pobla la app hidrologicas con datos de ejemplo.'

    def handle(self, *args, **options):
        # Hidrosuroeste
        gerente1, _ = Gerente.objects.get_or_create(
            nombre='Gerente Rando',
            cedula='10000001',
            telefono='0414-1234501'
        )
        self.stdout.write(self.style.SUCCESS(f'Gerente creado: {gerente1}'))

        hidrosuroeste, _ = Hidrologica.objects.get_or_create(
            nombre_delhidrologica='Hidrosuroeste',
            acronimo='HSO',
            rif='J-80000001-0',
            gerente_comercial_actual=gerente1,
            presidente_actual='Jose Fragozo',
            ciclo_lectura='01',
            url='https://hidrosuroeste.com',
            direccion_ip_publica='190.202.3.102',
            direccion_ip_privada='192.168.10.34',
            tipo_conexion='local',
        )
        if not hidrosuroeste.logo:
            from django.core.files import File
            import os
            logo_path = os.path.join('static', 'img', 'logo.png')
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    hidrosuroeste.logo.save('logo_hso.png', File(f), save=True)
        self.stdout.write(self.style.SUCCESS(f'Hidrológica creada: {hidrosuroeste}'))

        # Hidrocapital
        gerente2, _ = Gerente.objects.get_or_create(
            nombre='Gerente Rando',
            cedula='10000002',
            telefono='0414-1234502'
        )
        self.stdout.write(self.style.SUCCESS(f'Gerente creado: {gerente2}'))

        hidrocapital, _ = Hidrologica.objects.get_or_create(
            nombre_delhidrologica='Hidrocapital',
            acronimo='HC',
            rif='J-80000002-0',
            gerente_comercial_actual=gerente2,
            presidente_actual='Carlos Mars',
            ciclo_lectura='02',
            url='https://hidrocapital.com',
            direccion_ip_publica='190.202.5.141',
            direccion_ip_privada='10.10.10.111',
            direccion_ip_vpn='190.202.5.141',
            tipo_conexion='vpn',
        )
        if not hidrocapital.logo:
            from django.core.files import File
            import os
            logo_path = os.path.join('static', 'img', 'logo.png')
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    hidrocapital.logo.save('logo_hc.png', File(f), save=True)
        self.stdout.write(self.style.SUCCESS(f'Hidrológica creada: {hidrocapital}'))
