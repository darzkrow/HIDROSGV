from .models import Empresa

def empresa_context(request):
    empresa = Empresa.objects.first()
    return {'empresa_nombre': empresa.nombre if empresa else 'Sin Empresa'}
