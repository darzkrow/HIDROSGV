from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Ejecuta create_roles_permissions y populate_dashboard en un solo comando.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Ejecutando create_roles_permissions...'))
        call_command('create_roles_permissions')
        self.stdout.write(self.style.SUCCESS('Roles y permisos creados.'))
        self.stdout.write(self.style.WARNING('Ejecutando populate_dashboard...'))
        call_command('populate_dashboard')
        self.stdout.write(self.style.SUCCESS('Dashboard poblado correctamente.'))
