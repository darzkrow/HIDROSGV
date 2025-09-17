
"""
Serializadores para la API HIDROLOBI.
Permiten transformar los modelos en datos JSON para la API REST.
"""

# ===================== IMPORTS =====================
from rest_framework import serializers
from .models import Visitante, Carnet, Visita, Empleado, Piso, Oficina


class VisitanteSerializer(serializers.ModelSerializer):
    """
    Serializador de visitante: todos los campos.
    """
    class Meta:
        model = Visitante
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    """
    Serializador de empleado: todos los campos.
    """
    class Meta:
        model = Empleado
        fields = '__all__'

class PisoSerializer(serializers.ModelSerializer):
    """
    Serializador de piso: todos los campos.
    """
    class Meta:
        model = Piso
        fields = '__all__'

class OficinaSerializer(serializers.ModelSerializer):
    """
    Serializador de oficina: incluye piso anidado.
    """
    piso = PisoSerializer(read_only=True)
    class Meta:
        model = Oficina
        fields = '__all__'


class CarnetSerializer(serializers.ModelSerializer):
    """
    Serializador de carnet: incluye visitante anidado.
    """
    visitante = VisitanteSerializer(read_only=True)
    class Meta:
        model = Carnet
        fields = '__all__'


class VisitaSerializer(serializers.ModelSerializer):
    """
    Serializador de visita: incluye visitante, anfitrión, oficina y carnet anidados.
    """
    visitante = VisitanteSerializer(read_only=True)
    anfitrion = EmpleadoSerializer(read_only=True)
    oficina = OficinaSerializer(read_only=True)
    carnet = CarnetSerializer(read_only=True)
    class Meta:
        model = Visita
        fields = '__all__'
