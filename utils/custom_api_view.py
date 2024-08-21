from rest_framework.exceptions import (AuthenticationFailed, ErrorDetail,
                                       MethodNotAllowed, NotAuthenticated,
                                       NotFound, PermissionDenied,
                                       ValidationError)
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from rest_framework.views import APIView

from .custom_response import (BadRequestException, ForbiddenException,
                              InternalServerErrorException,
                              MethodNotAllowedException, NotFoundException,
                              UnauthorizedException)


class CustomResponseAPIView(APIView):
    def handle_exception(self, exc):
        message = self._extract_non_field_errors(exc.detail)

        if isinstance(exc, AuthenticationFailed) or isinstance(exc, NotAuthenticated):
            return UnauthorizedException(message=message)
        elif isinstance(exc, ValidationError):
            return BadRequestException(message=message)
        elif isinstance(exc, MethodNotAllowed):
            return MethodNotAllowedException(message=message)
        elif isinstance(exc, NotFound):
            return NotFoundException(message=message)
        elif isinstance(exc, PermissionDenied):
            return ForbiddenException(message=message)
        else:
            return InternalServerErrorException(message=message)

    def _extract_non_field_errors(self, detail):
        if isinstance(detail, dict):
            non_field_errors = detail.get('non_field_errors')
            if non_field_errors is not None:
                return self._format_errors(non_field_errors)
            return {key: self._extract_non_field_errors(value) for key, value in detail.items()}
        elif isinstance(detail, list) or isinstance(detail, ReturnList):
            return self._format_errors(detail)
        elif isinstance(detail, ErrorDetail):
            return str(detail)
        else:
            return str(detail)

    def _format_errors(self, errors):
        if isinstance(errors, list) or isinstance(errors, ReturnList):
            return ' '.join([str(e) for e in errors])
        elif isinstance(errors, dict) or isinstance(errors, ReturnDict):
            return ' '.join([self._format_errors(value) for value in errors.values()])
        elif isinstance(errors, ErrorDetail):
            return str(errors)
        else:
            return str(errors)
