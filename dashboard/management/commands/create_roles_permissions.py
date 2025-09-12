from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Crea los roles (grupos) y asigna permisos predeterminados.'

    def handle(self, *args, **options):
        # Crear grupos
        admin_group, _ = Group.objects.get_or_create(name='Administrador-IT')
        supervisor_group, _ = Group.objects.get_or_create(name='Supervisor')
        user_group, _ = Group.objects.get_or_create(name='User')

        # Permisos globales
        all_permissions = Permission.objects.all()
        # Permisos de solo lectura
        read_permissions = Permission.objects.filter(codename__startswith='view_')

        # Asignar permisos
        admin_group.permissions.set(all_permissions)
        supervisor_group.permissions.set(read_permissions)
        user_group.permissions.clear()  # Sin permisos especiales

        self.stdout.write(self.style.SUCCESS('Roles y permisos asignados correctamente:'))
        self.stdout.write(f'- Administrador-IT: todos los permisos')
        self.stdout.write(f'- Supervisor: solo permisos de lectura')
        self.stdout.write(f'- User: sin permisos especiales')
