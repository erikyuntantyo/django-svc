from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import ExpiringToken


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'
    model = ExpiringToken

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        if token.is_expired():
            raise AuthenticationFailed('Token has expired')

        return (token.user, token)
