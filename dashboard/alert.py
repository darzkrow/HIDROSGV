# alert.py
"""
Centraliza la generación de alertas SweetAlert para el dashboard.
"""

def sweetalert_success(message, title="Éxito", timer=2000):
    return {
        'swal': {
            'icon': 'success',
            'title': title,
            'text': message,
            'timer': timer,
        }
    }

def sweetalert_error(message, title="Error", timer=3000):
    return {
        'swal': {
            'icon': 'error',
            'title': title,
            'text': message,
            'timer': timer,
        }
    }

def sweetalert_warning(message, title="Advertencia", timer=2500):
    return {
        'swal': {
            'icon': 'warning',
            'title': title,
            'text': message,
            'timer': timer,
        }
    }

def sweetalert_info(message, title="Información", timer=2000):
    return {
        'swal': {
            'icon': 'info',
            'title': title,
            'text': message,
            'timer': timer,
        }
    }
