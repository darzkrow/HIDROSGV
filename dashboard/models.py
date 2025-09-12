from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
	email = models.EmailField('Correo electrónico', unique=True)

	groups = models.ManyToManyField(
		'auth.Group',
		related_name='dashboard_user_set',
		blank=True,
		help_text='Los grupos a los que pertenece este usuario.',
		verbose_name='grupos',
	)
	user_permissions = models.ManyToManyField(
		'auth.Permission',
		related_name='dashboard_user_permissions_set',
		blank=True,
		help_text='Permisos específicos para este usuario.',
		verbose_name='permisos de usuario',
	)

class Empresa(models.Model):
	nombre = models.CharField('Nombre de la empresa', max_length=100, unique=True)
	razon_social = models.CharField('Razón social', max_length=150, blank=True, null=True)
	rif = models.CharField('RIF', max_length=15, unique=True)
	titulo = models.CharField('Título del sistema', max_length=150)
	direccion = models.CharField('Dirección', max_length=200, blank=True, null=True)
	telefono = models.CharField('Teléfono', max_length=20, blank=True, null=True)
	email = models.EmailField('Email', blank=True, null=True)

	class Meta:
		verbose_name = 'Empresa'
		verbose_name_plural = 'Empresas'
		db_table = 'empresas'

	def __str__(self):
		return self.nombre


class UnidadOrganizativa(models.Model):
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='unidades')
	prefijo = models.CharField('Prefijo', max_length=10, unique=True)
	nombre = models.CharField('Nombre de la unidad', max_length=100, unique=True)
	descripcion = models.CharField('Descripción', max_length=200, blank=True, null=True)

	class Meta:
		verbose_name = 'Unidad Organizativa'
		verbose_name_plural = 'Unidades Organizativas'
		db_table = 'unidades_organizativas'

	def __str__(self):
		return f"({self.empresa.nombre}) # {self.prefijo} - {self.nombre}"


class Profile(models.Model):
	VENEZOLANO = 'V'
	EXTRANJERO = 'E'
	NAC_CHOICES = [
		(VENEZOLANO, 'Venezolano'),
		(EXTRANJERO, 'Extranjero'),
	]

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(blank=True, null=True)
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
	nac = models.CharField('Nacionalidad', max_length=1, choices=NAC_CHOICES)
	dni = models.IntegerField('Cédula', unique=True, null=True, blank=True)
	telefono = models.CharField('Teléfono', max_length=15, blank=True, null=True)
	must_change_password = models.BooleanField(default=False)
	password_expires_at = models.DateTimeField('Expira contraseña', blank=True, null=True)

	class Meta:
		verbose_name = 'Perfil'
		verbose_name_plural = 'Perfiles'
		db_table = 'profiles'

	def __str__(self):
		return f"Perfil de {self.user.username} - {self.user.first_name} {self.user.last_name}"

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
	if created:
		# No asignar dni por defecto para evitar colisiones
		Profile.objects.get_or_create(user=instance)
