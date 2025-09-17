from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from .models import Visitante, Carnet, Visita, Empleado, Piso, Oficina

admin.site.register(Visitante)
admin.site.register(Carnet)
admin.site.register(Visita)
admin.site.register(Empleado)
admin.site.register(Piso)
admin.site.register(Oficina)

# Script para crear roles y permisos básicos
class Command(BaseCommand):
	help = 'Crear grupos de roles y asignar permisos básicos'

	def handle(self, *args, **kwargs):
		roles = ['Administrador', 'Recepcionista', 'Visitante']
		for role in roles:
			group, created = Group.objects.get_or_create(name=role)
			if role == 'Administrador':
				group.permissions.set(Permission.objects.all())
			elif role == 'Recepcionista':
				perms = Permission.objects.filter(codename__in=[
					'add_visitante', 'change_visitante', 'view_visitante',
					'add_visita', 'change_visita', 'view_visita',
					'add_carnet', 'change_carnet', 'view_carnet',
				])
				group.permissions.set(perms)
			elif role == 'Visitante':
				perms = Permission.objects.filter(codename__in=[
					'view_visitante', 'view_visita',
				])
				group.permissions.set(perms)
		self.stdout.write(self.style.SUCCESS('Grupos y permisos creados correctamente.'))
