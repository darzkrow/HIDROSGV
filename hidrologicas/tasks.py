from celery import shared_task
from django.core.management import call_command

@shared_task
def tarea_chequear_conexion_hidrologicas():
    call_command('chequear_conexion_hidrologicas')
