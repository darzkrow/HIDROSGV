#!/bin/bash
# Script para instalar y configurar Supervisor, Celery y Redis para HIDROSGV
set -e

# 1. Instalar Redis
if ! command -v redis-server &> /dev/null; then
    echo "Instalando Redis..."
    sudo apt-get update
    sudo apt-get install -y redis-server
    sudo systemctl enable redis-server
    sudo systemctl start redis-server
else
    echo "Redis ya está instalado."
fi

# 2. Crear entorno virtual si no existe
if [ ! -d "../venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv ../venv
fi
source ../venv/bin/activate

# 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# 4. Migraciones Django
cd ..
echo "Ejecutando migraciones Django..."
python manage.py migrate
cd supervisorctl

# 5. Configuración Supervisor
if ! command -v supervisord &> /dev/null; then
    echo "Instalando Supervisor..."
    sudo apt-get install -y supervisor
fi

sudo cp supervisord.conf /etc/supervisor/conf.d/hidrosgv.conf

# 7. Recargar y reiniciar Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart all

# 8. Mensaje final
echo "Supervisor, Celery y Gunicorn configurados correctamente."
echo "Puedes verificar los procesos con: sudo supervisorctl status"
