# Configuración de Supervisor y Celery

Esta carpeta contiene los archivos necesarios para ejecutar tareas programadas con Celery y supervisarlas con Supervisor.

## Estructura
- `supervisord.conf`: Configuración principal de Supervisor.
- `celery.conf`: Configuración del proceso Celery.
- `start_celery.sh`: Script para iniciar el worker de Celery.
- `requirements.txt`: Dependencias necesarias para Celery y Supervisor.

## Tarea programada
La tarea de verificación de conexión de hidrológicas se ejecutará cada 1 hora usando Celery Beat.


## Instalación automática
Ejecuta el siguiente script para instalar y configurar todo:

```bash
bash setup_supervisor_celery.sh
```

Esto instalará Redis, Gunicorn, Supervisor, Celery y configurará los procesos necesarios.

## Procesos gestionados
- **Gunicorn**: Ejecuta el proyecto Django en modo producción.
- **Celery**: Ejecuta tareas asíncronas.
- **Celery Beat**: Programa la tarea de verificación cada 1 hora.

## Comandos útiles
- Ver estado de los procesos:
	```bash
	sudo supervisorctl status
	```
- Reiniciar todos los procesos:
	```bash
	sudo supervisorctl restart all
	```
- Ver logs:
	```bash
	tail -f /tmp/gunicorn.out.log
	tail -f /tmp/celery.out.log
	tail -f /tmp/celerybeat.out.log
	```

## Archivos
- `supervisord.conf`: Configura los procesos de Celery y Celery Beat.
- `celery.conf`: Configura el worker de Celery.
- `start_celery.sh`: Script para iniciar Celery con el entorno adecuado.
- `requirements.txt`: Incluye celery, supervisor y librerías necesarias.
