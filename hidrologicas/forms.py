from django import forms
from .models import Hidrologica, Gerente

class GerenteForm(forms.ModelForm):
    class Meta:
        model = Gerente
        fields = ['nombre', 'cedula', 'telefono']

class HidrologicaForm(forms.ModelForm):
    class Meta:
        model = Hidrologica
        fields = ['nombre_delhidrologica', 'acronimo', 'rif', 'ciclo_lectura', 'logo', 'direccion_ip_publica', 'direccion_ip_privada', 'tipo_conexion', 'url']
