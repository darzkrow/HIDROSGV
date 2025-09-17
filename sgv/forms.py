
"""
Formularios para la gestión web de visitantes y visitas en HIDROLOBI.
"""

# ===================== IMPORTS =====================
from django import forms
from .models import Visitante, Visita, Empleado, Oficina

class VisitanteForm(forms.ModelForm):
    """
    Formulario para registrar y editar visitantes.
    """
    class Meta:
        model = Visitante
        fields = ['nombre_completo', 'identificacion', 'contacto', 'empresa', 'telefono', 'correo', 'foto']

class VisitaForm(forms.ModelForm):
    """
    Formulario para registrar y editar visitas.
    """
    placa_vehiculo = forms.CharField(required=False)
    class Meta:
        model = Visita
        fields = ['visitante', 'motivo', 'anfitrion', 'oficina', 'foto', 'placa_vehiculo']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['anfitrion'].queryset = Empleado.objects.filter(activo=True)
        self.fields['oficina'].queryset = Oficina.objects.all()
