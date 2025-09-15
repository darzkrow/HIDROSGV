from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
def hidrologicas_status_api(request):
    hidros = Hidrologica.objects.all()
    data = []
    for h in hidros:
        data.append({
            'id': h.id,
            'estado_conexion': h.estado_conexion,
            'latencia_ms': h.latencia_ms,
        })
    return JsonResponse({'hidrologicas': data})
from django.shortcuts import get_object_or_404

@login_required
def hidrologica_detail(request, pk):
    h = get_object_or_404(Hidrologica, pk=pk)
    user = request.user
    es_admin = user.is_superuser or user.groups.filter(name__in=['Administrador-IT','Supervisor']).exists()
    return render(request, 'hidrologicas/detail.html', {'h': h, 'es_admin': es_admin})
from .forms import GerenteForm

@login_required
def gerente_create(request):
    if request.method == 'POST':
        form = GerenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hidrologica_list')
    else:
        form = GerenteForm()
    return render(request, 'hidrologicas/gerente_create.html', {'form': form})
from django.shortcuts import render
from .models import Hidrologica

@login_required
def hidrologica_list(request):
    hidrologicas = list(Hidrologica.objects.all())
    filas = [hidrologicas[i:i+5] for i in range(0, len(hidrologicas), 5)]
    user = request.user
    es_admin = user.is_superuser or user.groups.filter(name__in=['Administrador-IT','Supervisor']).exists()
    return render(request, 'hidrologicas/list.html', {'filas': filas, 'es_admin': es_admin})

from .forms import HidrologicaForm

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name__in=['Administrador-IT','Supervisor']).exists())
def hidrologica_create(request):
    if request.method == 'POST':
        form = HidrologicaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hidrologica_list')
    else:
        form = HidrologicaForm()
    return render(request, 'hidrologicas/create.html', {'form': form})

from django.shortcuts import get_object_or_404, redirect

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name__in=['Administrador-IT','Supervisor']).exists())
def hidrologica_update(request, pk):
    hidrologica = get_object_or_404(Hidrologica, pk=pk)
    if request.method == 'POST':
        form = HidrologicaForm(request.POST, instance=hidrologica)
        if form.is_valid():
            form.save()
            return redirect('hidrologica_list')
    else:
        form = HidrologicaForm(instance=hidrologica)
    return render(request, 'hidrologicas/update.html', {'form': form, 'hidrologica': hidrologica})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name__in=['Administrador-IT','Supervisor']).exists())
def hidrologica_delete(request, pk):
    hidrologica = get_object_or_404(Hidrologica, pk=pk)
    if request.method == 'POST':
        hidrologica.delete()
        return redirect('hidrologica_list')
    return render(request, 'hidrologicas/delete.html', {'hidrologica': hidrologica})
