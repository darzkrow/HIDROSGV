from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth import logout
from django.urls import resolve

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout = getattr(settings, 'SESSION_INACTIVITY_TIMEOUT', 90)  # 90 segundos por defecto

    def __call__(self, request):
        print(f"[SessionTimeoutMiddleware] Timeout configurado: {self.timeout} segundos")  # Depuración
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            now = timezone.now().timestamp()
            # Bloqueo por inactividad
            if last_activity:
                elapsed = now - last_activity
                if elapsed > self.timeout:
                    logout(request)
                    request.session['session_blocked'] = True
                    return redirect('session_blocked')
            request.session['last_activity'] = now

            # Bloqueo de múltiples sesiones
            session_key = request.session.session_key
            from django.contrib.sessions.models import Session
            user_sessions = Session.objects.filter(expire_date__gte=timezone.now())
            user_sessions = [s for s in user_sessions if s.get_decoded().get('_auth_user_id') == str(request.user.id)]
            if len(user_sessions) > 1:
                # Si hay más de una sesión activa para el usuario, cerrar la actual
                logout(request)
                request.session['session_blocked'] = True
                return redirect('session_blocked')
        else:
            request.session.pop('last_activity', None)
        response = self.get_response(request)
        return response

class ForceLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_paths = ['index', 'login', 'register', 'admin:login', 'session_blocked']
        current_url = resolve(request.path_info).url_name
        if not request.user.is_authenticated and current_url not in public_paths:
            return redirect('/')
        return self.get_response(request)
