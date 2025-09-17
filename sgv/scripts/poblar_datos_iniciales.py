from registro.models import Piso, Oficina, Empleado

def poblar():
    # Crear pisos
    piso1 = Piso.objects.get_or_create(numero='1')[0]
    piso2 = Piso.objects.get_or_create(numero='2')[0]

    # Crear oficinas
    oficinas = [
        ('Administración', piso1),
        ('Talento Humano', piso1),
        ('Sistemas', piso2),
        ('Finanzas', piso2),
    ]
    for nombre, piso in oficinas:
        Oficina.objects.get_or_create(nombre=nombre, piso=piso)

    # Crear empleados
    empleados = [
        ('Ana Pérez', '1001'),
        ('Luis Gómez', '1002'),
        ('María Torres', '1003'),
        ('Carlos Ruiz', '1004'),
    ]
    for nombre, identificacion in empleados:
        Empleado.objects.get_or_create(nombre_completo=nombre, identificacion=identificacion, activo=True)

if __name__ == '__main__':
    poblar()
    print('Datos iniciales cargados.')
