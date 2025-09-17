from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncQuarter, TruncYear
from django.db.models import Count
import datetime
from django.http import JsonResponse, HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
import io
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.shortcuts import render, redirect
from .forms import VisitanteForm, VisitaForm
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Visitante, Carnet, Visita, Empleado, Piso, Oficina
from .serializers import VisitanteSerializer, CarnetSerializer, VisitaSerializer, EmpleadoSerializer, PisoSerializer, OficinaSerializer
from django.db.models import Q
from django.views import View
@login_required
@permission_required('sgv.view_visita', raise_exception=True)
def estadisticas_acceso(request):
	# Filtros
	fecha_inicio = request.GET.get('fecha_inicio')
	fecha_fin = request.GET.get('fecha_fin')
	agrupacion = request.GET.get('agrupacion', 'diario')
	exportar = request.GET.get('exportar')  # 'excel' o 'pdf'
	qs = Visita.objects.all()
	if fecha_inicio:
		qs = qs.filter(fecha_entrada__date__gte=fecha_inicio)
	if fecha_fin:
		qs = qs.filter(fecha_entrada__date__lte=fecha_fin)
	# Agrupación
	if agrupacion == 'diario':
		qs = qs.annotate(periodo=TruncDay('fecha_entrada'))
	elif agrupacion == 'semanal':
		qs = qs.annotate(periodo=TruncWeek('fecha_entrada'))
	elif agrupacion == 'quincenal':
		# Agrupación quincenal manual
		qs = qs.annotate(periodo=TruncMonth('fecha_entrada'))
	elif agrupacion == 'mensual':
		qs = qs.annotate(periodo=TruncMonth('fecha_entrada'))
	elif agrupacion == 'trimestral':
		qs = qs.annotate(periodo=TruncQuarter('fecha_entrada'))
	elif agrupacion == 'anual':
		qs = qs.annotate(periodo=TruncYear('fecha_entrada'))
	else:
		qs = qs.annotate(periodo=TruncDay('fecha_entrada'))
	estadisticas = qs.values('periodo').annotate(total=Count('id')).order_by('periodo')
	# Exportar
	if exportar == 'excel':
		df = pd.DataFrame(list(estadisticas))
		output = io.BytesIO()
		with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
			df.to_excel(writer, index=False)
		output.seek(0)
		response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = 'attachment; filename=estadisticas_acceso.xlsx'
		return response
	if exportar == 'pdf':
		df = pd.DataFrame(list(estadisticas))
		plt.figure(figsize=(10,5))
		plt.bar(df['periodo'].astype(str), df['total'])
		plt.xticks(rotation=45)
		plt.title('Accesos por periodo')
		plt.tight_layout()
		buf = io.BytesIO()
		plt.savefig(buf, format='pdf')
		buf.seek(0)
		response = HttpResponse(buf.read(), content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=estadisticas_acceso.pdf'
		return response
	# Renderizar tabla y gráfico en template
	context = {
		'estadisticas': estadisticas,
		'agrupacion': agrupacion,
		'fecha_inicio': fecha_inicio,
		'fecha_fin': fecha_fin,
	}
	return render(request, 'sgv/estadisticas_acceso.html', context)



@login_required
@permission_required('sgv.view_visitante', raise_exception=True)
def detalle_visitante(request, visitante_id):
	"""
	Vista protegida: solo usuarios con permiso 'view_visitante' pueden acceder.
	Recomendado para recepcionistas y administradores.
	"""
	visitante = get_object_or_404(Visitante, id=visitante_id)
	visitas = Visita.objects.filter(visitante=visitante).order_by('-fecha_entrada')
	if request.method == 'POST':
		form = VisitanteForm(request.POST, instance=visitante)
		if form.is_valid():
			form.save()
	else:
		form = VisitanteForm(instance=visitante)
	return render(request, 'registro/detalle_visitante.html', {
		'visitante': visitante,
		'form': form,
		'visitas': visitas
	})
@login_required
@permission_required('sgv.view_visitante', raise_exception=True)
def buscar_visitante(request):
	"""
	Vista protegida: solo usuarios con permiso 'view_visitante'.
	"""
	identificacion = request.GET.get('identificacion')
	carnet_num = request.GET.get('carnet')
	# Buscar por carnet
	if carnet_num:
		visita_activa = Visita.objects.filter(carnet__numero=carnet_num, fecha_salida__isnull=True).first()
		if visita_activa:
			# Redirigir a registrar salida del visitante que tiene el carnet
			return redirect('sgv:registrar-salida', visita_id=visita_activa.id)
		else:
			return render(request, 'registro/buscar_visitante.html', {'mensaje': 'No hay visita activa para ese carnet.'})
	# Buscar por identificación
	if identificacion:
		try:
			visitante = Visitante.objects.get(identificacion=identificacion)
			visita_activa = Visita.objects.filter(visitante=visitante, fecha_salida__isnull=True).first()
			if visita_activa:
				# Redirigir a registrar salida y luego mostrar formulario para nueva visita
				return redirect('sgv:registrar-salida', visita_id=visita_activa.id)
			else:
				# Redirigir a detalle para registrar nueva visita
				return redirect('sgv:detalle-visitante', visitante_id=visitante.id)
		except Visitante.DoesNotExist:
			# Redirigir a formulario combinado para registrar visitante y visita
			return redirect('sgv:registro-visitante-nuevo', identificacion=identificacion)
	return render(request, 'registro/buscar_visitante.html')

@login_required
@permission_required('sgv.view_visita', raise_exception=True)
def buscar_visita(request):
	"""
	Vista protegida: solo usuarios con permiso 'view_visita'.
	"""
	visitas = None
	q = request.GET.get('q')
	fecha = request.GET.get('fecha')
	carnet_num = request.GET.get('carnet')
	qs = Visita.objects.all()
	if q:
		qs = qs.filter(
			Q(visitante__nombre_completo__icontains=q) |
			Q(motivo__icontains=q) |
			Q(oficina__nombre__icontains=q) |
			Q(anfitrion__nombre_completo__icontains=q) |
			Q(visitante__identificacion__icontains=q) |
			Q(carnet__numero__icontains=q)
		)
	if fecha:
		fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
		qs = qs.filter(fecha_entrada__date=fecha_dt.date())
	if carnet_num:
		qs = qs.filter(carnet__numero=carnet_num)
	visitas = qs if (q or fecha or carnet_num) else None
	return render(request, 'registro/buscar_visita.html', {'visitas': visitas})

@csrf_exempt
@login_required
@permission_required('sgv.change_visita', raise_exception=True)
def registrar_salida(request, visita_id):
	"""
	Solo recepcionistas y administradores pueden registrar la salida de una visita.
	"""
	visita = Visita.objects.get(id=visita_id)
	if request.method == 'POST' and not visita.fecha_salida:
		visita.fecha_salida = timezone.now()
		if visita.carnet:
			visita.carnet.estado = 'disponible'
			visita.carnet.visitante = None
			visita.carnet.save()
		visita.save()
	return HttpResponseRedirect(reverse('sgv:buscar-visita'))

# Vista Dashboard
class DashboardView(View):
	"""
	Dashboard protegido: solo usuarios autenticados pueden ver métricas.
	"""
	@method_decorator(login_required)
	def get(self, request):
		from .models import Visitante, Empleado, Oficina, Visita
		context = {
			'visitantes_count': Visitante.objects.count(),
			'empleados_count': Empleado.objects.filter(activo=True).count(),
			'oficinas_count': Oficina.objects.count(),
			'visitas_count': Visita.objects.count(),
		}
		return render(request, 'registro/lobby.html', context)


# Vista para registrar visitante
@login_required
@permission_required('sgv.add_visitante', raise_exception=True)
def registrar_visitante(request, identificacion=None):
	"""
	Solo recepcionistas y administradores pueden registrar nuevos visitantes.
	"""
	if request.method == 'POST':
		form = VisitanteForm(request.POST, request.FILES)
		if form.is_valid():
			visitante = form.save(commit=False)
			foto = request.FILES.get('foto')
			if foto:
				ext = foto.name.split('.')[-1]
				filename = f"{visitante.identificacion}.{ext}"
				visitante.foto.save(filename, foto)
			visitante.save()
			return redirect('sgv:registro-visita')
	else:
		form = VisitanteForm()
	return render(request, 'registro/registrar_visitante.html', {'form': form, 'identificacion': identificacion})

# Vista para registrar visita
@login_required
@permission_required('sgv.add_visita', raise_exception=True)
def registrar_visita(request, visitante_id=None):
	"""
	Solo recepcionistas y administradores pueden registrar nuevas visitas.
	"""
	visita_activa = None
	visitante = None
	if visitante_id:
		try:
			visitante = Visitante.objects.get(id=visitante_id)
			visita_activa = Visita.objects.filter(visitante=visitante, fecha_salida__isnull=True).first()
		except Visitante.DoesNotExist:
			visitante = None
	carnet_asignado = None
	if request.method == 'POST':
		form = VisitaForm(request.POST, request.FILES)
		# Forzar queryset de campos select
		form.fields['anfitrion'].queryset = Empleado.objects.filter(activo=True)
		form.fields['oficina'].queryset = Oficina.objects.all()
		if form.is_valid() and not visita_activa:
			visita = form.save(commit=False)
			import random
			carnets_disponibles = list(Carnet.objects.filter(estado='disponible'))
			carnet = random.choice(carnets_disponibles) if carnets_disponibles else None
			if carnet:
				visita.carnet = carnet
				carnet.estado = 'asignado'
				carnet.visitante = visita.visitante
				carnet.save()
				carnet_asignado = carnet.numero
			visita.save()
			return render(request, 'registro/registrar_visita.html', {
				'form': VisitaForm(),
				'mensaje': None,
				'carnet_asignado': carnet_asignado,
				'visitante': visitante
			})
	else:
		initial = {'visitante': visitante.id} if visitante else None
		form = VisitaForm(initial=initial)
		form.fields['anfitrion'].queryset = Empleado.objects.filter(activo=True)
		form.fields['oficina'].queryset = Oficina.objects.all()
		if visitante:
			form.fields['visitante'].disabled = True
	return render(request, 'registro/registrar_visita.html', {
		'form': form,
		'mensaje': None,
		'carnet_asignado': carnet_asignado,
		'visitante': visitante
	})
from django.utils.decorators import method_decorator

# Vista de listado de visitas protegida
@method_decorator([login_required, permission_required('sgv.view_visita', raise_exception=True)], name='dispatch')
class ListaVisitasView(ListView):
	"""
	Solo usuarios con permiso 'view_visita' pueden ver el listado de visitas.
	Recomendado para recepcionistas y administradores.
	"""
	model = Visita
	template_name = 'registro/lista_visitas.html'
	context_object_name = 'visitas'




from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

# API: ViewSet de Visitante protegido
class VisitanteViewSet(viewsets.ModelViewSet):
	"""
	API protegida: solo usuarios autenticados y con permisos pueden acceder.
	Permisos gestionados por grupos (Administrador, Recepcionista, Visitante).
	"""
	queryset = Visitante.objects.all()
	serializer_class = VisitanteSerializer
	permission_classes = [IsAuthenticated, DjangoModelPermissions]

    
# API: ViewSet de Visita protegido
class VisitaViewSet(viewsets.ModelViewSet):
	"""
	API protegida: solo usuarios autenticados y con permisos pueden acceder.
	Permisos gestionados por grupos (Administrador, Recepcionista).
	"""
	queryset = Visita.objects.all()
	serializer_class = VisitaSerializer
	permission_classes = [IsAuthenticated, DjangoModelPermissions]

	def create(self, request, *args, **kwargs):
		carnet = Carnet.objects.filter(estado='disponible').first()
		if not carnet:
			return Response({'error': 'No hay carnets disponibles.'}, status=status.HTTP_400_BAD_REQUEST)
		data = request.data.copy()
		# Permitir registrar por número de identificación
		visitante_id = data.get('visitante')
		visitante_identificacion = data.get('visitante_identificacion')
		if visitante_identificacion:
			try:
				visitante = Visitante.objects.get(identificacion=visitante_identificacion)
				visitante_id = visitante.id
			except Visitante.DoesNotExist:
				return Response({'error': 'Visitante no encontrado.'}, status=status.HTTP_400_BAD_REQUEST)
		oficina_id = data.get('oficina')
		anfitrion_id = data.get('anfitrion')
		anfitrion_identificacion = data.get('anfitrion_identificacion')
		if anfitrion_identificacion:
			try:
				anfitrion = Empleado.objects.get(identificacion=anfitrion_identificacion)
				anfitrion_id = anfitrion.id
			except Empleado.DoesNotExist:
				return Response({'error': 'Anfitrión no encontrado.'}, status=status.HTTP_400_BAD_REQUEST)
		motivo = data.get('motivo')
		foto = data.get('foto')
		placa_vehiculo = data.get('placa_vehiculo')
		if not visitante_id or not oficina_id or not anfitrion_id:
			return Response({'error': 'Debe especificar visitante, oficina y anfitrión.'}, status=status.HTTP_400_BAD_REQUEST)
		visita = Visita.objects.create(
			visitante_id=visitante_id,
			oficina_id=oficina_id,
			anfitrion_id=anfitrion_id,
			motivo=motivo,
			foto=foto,
			carnet=carnet,
			placa_vehiculo=placa_vehiculo
		)
		carnet.estado = 'asignado'
		carnet.visitante_id = visitante_id
		carnet.save()
		serializer = VisitaSerializer(visita)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	
class EmpleadoViewSet(viewsets.ModelViewSet):
	queryset = Empleado.objects.filter(activo=True)
	serializer_class = EmpleadoSerializer

class PisoViewSet(viewsets.ModelViewSet):
	queryset = Piso.objects.all()
	serializer_class = PisoSerializer

class OficinaViewSet(viewsets.ModelViewSet):
	queryset = Oficina.objects.all()
	serializer_class = OficinaSerializer

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		# Si se marca salida, liberar carnet
		fecha_salida = request.data.get('fecha_salida')
		if fecha_salida and not instance.fecha_salida:
			instance.fecha_salida = timezone.now()
			if instance.carnet:
				instance.carnet.estado = 'disponible'
				instance.carnet.visitante = None
				instance.carnet.save()
			instance.save()
		return super().update(request, *args, **kwargs)

class CarnetViewSet(viewsets.ModelViewSet):
	queryset = Carnet.objects.all()
	serializer_class = CarnetSerializer

class VisitanteHistorialView(generics.ListAPIView):
	serializer_class = VisitaSerializer

	def get_queryset(self):
		visitante_id = self.kwargs['pk']
		return Visita.objects.filter(visitante_id=visitante_id)

class CarnetDisponiblesView(APIView):
	def get(self, request):
		carnets = Carnet.objects.filter(estado='disponible')
		serializer = CarnetSerializer(carnets, many=True)
		return Response(serializer.data)

class CarnetDetalleView(APIView):
	def get(self, request, numero_carnet):
		try:
			carnet = Carnet.objects.get(numero=numero_carnet)
		except Carnet.DoesNotExist:
			return Response({'error': 'Carnet no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
		data = CarnetSerializer(carnet).data
		if carnet.visitante:
			data['visitante'] = VisitanteSerializer(carnet.visitante).data
		else:
			data['visitante'] = None
		return Response(data)
