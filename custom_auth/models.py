from django.utils import timezone
from rest_framework.authtoken.models import Token


class ExpiringToken(Token):
    proxy = True

    def is_expired(self):
        return self.created + timezone.timedelta(minutes=5) < timezone.now()
