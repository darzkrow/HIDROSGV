
from django.contrib import admin

from .models import Profile, Empresa, UnidadOrganizativa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'titulo', 'telefono', 'email')

@admin.register(UnidadOrganizativa)
class UnidadOrganizativaAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'empresa', 'descripcion')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'bio')
