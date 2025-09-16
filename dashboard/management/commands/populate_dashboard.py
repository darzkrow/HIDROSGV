from django.core.management.base import BaseCommand
from dashboard.models import User
from dashboard.models import Empresa, UnidadOrganizativa, Profile

class Command(BaseCommand):
    help = 'Pobla las tablas de dashboard con datos de ejemplo.'

    def handle(self, *args, **options):
        # Crear empresa
        empresa, _ = Empresa.objects.get_or_create(
            nombre='Empresa Ejemplo',
            razon_social='Empresa Ejemplo S.A.',
            rif='J-12345678-9',
            titulo='Sistema de Prueba',
            direccion='Calle Falsa 123',
            telefono='0212-1234567',
            email='info@ejemplo.com'
        )
        self.stdout.write(self.style.SUCCESS(f'Empresa creada: {empresa}'))

        # Crear unidades organizativas
        unidad1, _ = UnidadOrganizativa.objects.get_or_create(
            empresa=empresa,
            prefijo='ADM',
            nombre='Administración',
            descripcion='Oficina administrativa'
        )
        unidad2, _ = UnidadOrganizativa.objects.get_or_create(
            empresa=empresa,
            prefijo='TEC',
            nombre='Tecnología',
            descripcion='Departamento de tecnología'
        )
        self.stdout.write(self.style.SUCCESS(f'Unidades creadas: {unidad1}, {unidad2}'))

        # Crear departamentos
        from dashboard.models import Departamento, Cargo
        departamento1, _ = Departamento.objects.get_or_create(
            unidad=unidad1,
            nombre='Contabilidad',
            descripcion='Departamento de contabilidad'
        )
        departamento2, _ = Departamento.objects.get_or_create(
            unidad=unidad2,
            nombre='Sistemas',
            descripcion='Departamento de sistemas'
        )
        self.stdout.write(self.style.SUCCESS(f'Departamentos creados: {departamento1}, {departamento2}'))

        # Crear cargos
        cargo1, _ = Cargo.objects.get_or_create(
            departamento=departamento1,
            nombre='Contador',
            descripcion='Responsable de la contabilidad'
        )
        cargo2, _ = Cargo.objects.get_or_create(
            departamento=departamento2,
            nombre='Analista de Sistemas',
            descripcion='Responsable de sistemas y soporte'
        )
        self.stdout.write(self.style.SUCCESS(f'Cargos creados: {cargo1}, {cargo2}'))

        # Crear usuarios y perfiles
        # Crear usuario administrador
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                password='123456789',
                first_name='Admin',
                last_name='Principal',
                email='admin@ejemplo.com'
            )
            profile, created = Profile.objects.get_or_create(user=admin)
            profile.bio = 'Administrador del sistema'
            profile.telefono = '0414-9999999'
            profile.nac = Profile.VENEZOLANO
            profile.dni = 99999999
            profile.save()
            self.stdout.write(self.style.SUCCESS('Usuario administrador creado: admin'))
        else:
            self.stdout.write(self.style.WARNING('El usuario administrador ya existe'))

        for i in range(1, 10):
            username = f'usuario{i}'
            dni = 12345000 + i
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password='123456789',
                    first_name=f'Nombre{i}',
                    last_name=f'Apellido{i}',
                    email=f'usuario{i}@ejemplo.com'
                )
                profile, created = Profile.objects.get_or_create(user=user)
                profile.bio = f'Bio del usuario {i}'
                profile.telefono = f'0414-00000{i}'
                profile.nac = Profile.VENEZOLANO
                profile.dni = dni
                profile.save()
                self.stdout.write(self.style.SUCCESS(f'Usuario y perfil creados: {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Usuario ya existe: {username}'))
