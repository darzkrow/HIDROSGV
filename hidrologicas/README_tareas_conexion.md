# Instrucciones para tareas programadas

# 1. Tarea por cron (management command)
# Ejecuta cada 10 minutos:
# */10 * * * * /ruta/a/tu/python /ruta/a/manage.py chequear_conexion_hidrologicas

# 2. Tarea Celery (para producción)
# Agrega en tu configuración Celery Beat:
# from hidrologicas.tasks import tarea_chequear_conexion_hidrologicas
# CELERY_BEAT_SCHEDULE = {
#     'chequear-conexion-hidrologicas-cada-10min': {
#         'task': 'hidrologicas.tasks.tarea_chequear_conexion_hidrologicas',
#         'schedule': 600.0,
#     },
# }

# Ambas tareas actualizan el estado de conexión de cada hidrológica y permiten mostrar el badge offline en la lista.
