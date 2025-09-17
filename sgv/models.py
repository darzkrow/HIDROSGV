"""
Modelos principales del sistema HIDROLOBI.
Cada modelo representa una entidad clave en el flujo de registro y control de visitantes.
"""

# ===================== IMPORTS =====================
from django.db import models
from .models_audit import AuditModel

# ===================== MODELOS =====================

class Visitante(AuditModel):
	"""
	Modelo de visitante: almacena datos personales y foto.
	"""
	nombre_completo = models.CharField(max_length=150, blank=True, null=True)
	identificacion = models.CharField(max_length=50, unique=True)
	contacto = models.CharField(max_length=30, blank=True, null=True)
	empresa = models.CharField(max_length=100, blank=True, null=True)
	telefono = models.CharField(max_length=20, blank=True, null=True)
	correo = models.EmailField(blank=True, null=True)
	foto = models.ImageField(upload_to='visitantes/', blank=True, null=True)

	def __str__(self):
		return f"{self.nombre_completo} ({self.identificacion})"

	class Meta:
		verbose_name = 'Visitante'
		verbose_name_plural = 'Visitantes'
		db_table = 'sgv.visitante'

class Carnet(AuditModel):
	"""
	Modelo de carnet temporal: asignación y estado.
	"""
	ESTADO_CHOICES = [
		('disponible', 'Disponible'),
		('asignado', 'Asignado'),
	]
	numero = models.CharField(max_length=3, unique=True)
	estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='disponible')
	visitante = models.ForeignKey('Visitante', null=True, blank=True, on_delete=models.SET_NULL)

	def __str__(self):
		return f"Carnet {self.numero} - {self.estado}"

	class Meta:
		verbose_name = 'Carnet'
		verbose_name_plural = 'Carnets'
		db_table = 'sgv.carnet'

class Visita(AuditModel):
	"""
	Modelo de visita: vincula visitante, anfitrión, oficina y carnet.
	"""
	visitante = models.ForeignKey('Visitante', on_delete=models.CASCADE)
	fecha_entrada = models.DateTimeField(auto_now_add=True)
	fecha_salida = models.DateTimeField(null=True, blank=True)
	motivo = models.CharField(max_length=255)
	anfitrion = models.ForeignKey('Empleado', on_delete=models.SET_NULL, null=True)
	oficina = models.ForeignKey('Oficina', on_delete=models.SET_NULL, null=True)
	foto = models.ImageField(upload_to='fotos/', null=True, blank=True)
	carnet = models.ForeignKey('Carnet', on_delete=models.SET_NULL, null=True)
	placa_vehiculo = models.CharField(max_length=20, blank=True, null=True)

	def __str__(self):
		return f"Visita de {self.visitante} a {self.oficina} ({self.fecha_entrada})"

	class Meta:
		verbose_name = 'Visita'
		verbose_name_plural = 'Visitas'
		db_table = 'sgv.visita'

class Empleado(AuditModel):
	"""
	Modelo de empleado (anfitrión): datos y estado.
	"""
	nombre_completo = models.CharField(max_length=150)
	identificacion = models.CharField(max_length=50, unique=True)
	activo = models.BooleanField(default=True)

	def __str__(self):
		return self.nombre_completo

	class Meta:
		verbose_name = 'Empleado'
		verbose_name_plural = 'Empleados'
		db_table = 'sgv.empleado'

class Piso(AuditModel):
	"""
	Modelo de piso: número y nombre descriptivo.
	"""
	numero = models.CharField(max_length=10)
	nombre = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return f"Piso {self.numero} {self.nombre if self.nombre else ''}".strip()

	class Meta:
		verbose_name = 'Piso'
		verbose_name_plural = 'Pisos'
		db_table = 'sgv.piso'

class Oficina(AuditModel):
	"""
	Modelo de oficina: nombre y relación con piso.
	"""
	nombre = models.CharField(max_length=100)
	piso = models.ForeignKey('Piso', on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.nombre} (Piso {self.piso.numero})"

	class Meta:
		verbose_name = 'Oficina'
		verbose_name_plural = 'Oficinas'
		db_table = 'sgv.oficina'
