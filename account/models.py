import uuid

from bson import ObjectId
from django.conf import settings
from django.db.models import (CASCADE, CharField, DateTimeField, ForeignKey,
                              Model, UUIDField)
from django.utils import timezone


class RefreshToken(Model):
    _id = CharField(primary_key=True, default=ObjectId,
                    editable=False, max_length=24)
    user = ForeignKey(settings.AUTH_USER_MODEL,
                      on_delete=CASCADE)
    token = UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = DateTimeField(auto_now_add=True)
    expires_at = DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=7)

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.token)
