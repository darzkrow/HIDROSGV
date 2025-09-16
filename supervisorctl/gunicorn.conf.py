# gunicorn.conf.py - Configuración recomendada para producción

bind = "0.0.0.0:8000"
workers = 3
worker_class = "sync"
max_requests = 1000
max_requests_jitter = 50
accesslog = "/tmp/gunicorn.access.log"
errorlog = "/tmp/gunicorn.error.log"
loglevel = "info"
timeout = 60
keepalive = 2
preload_app = True

# Puedes agregar más opciones según tus necesidades
