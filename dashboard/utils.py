from django.contrib.sessions.models import Session
from django.utils import timezone

from .models import User


def get_connected_user_ids():
    """Devuelve una lista de IDs de usuarios con sesiones activas."""
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    ids = []
    for s in sessions:
        try:
            data = s.get_decoded()
        except Exception:
            continue
        uid = data.get('_auth_user_id')
        if uid:
            try:
                ids.append(int(uid))
            except (TypeError, ValueError):
                continue
    return list(set(ids))


def get_connected_users():
    ids = get_connected_user_ids()
    if not ids:
        return User.objects.none()
    return User.objects.filter(id__in=ids)


def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR', '')
    return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')
