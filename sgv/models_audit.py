from django.db import models
from django.contrib.auth import get_user_model

class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(get_user_model(), null=True, blank=True, related_name="created_%(class)s_set", on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(get_user_model(), null=True, blank=True, related_name="updated_%(class)s_set", on_delete=models.SET_NULL)
    deleted_by = models.ForeignKey(get_user_model(), null=True, blank=True, related_name="deleted_%(class)s_set", on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
