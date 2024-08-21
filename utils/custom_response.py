import logging

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
                                   HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
                                   HTTP_405_METHOD_NOT_ALLOWED,
                                   HTTP_500_INTERNAL_SERVER_ERROR)

logger = logging.getLogger(__name__)


class CreatedResponse(Response):
    def __init__(self, result=None):
        super().__init__(data=result, status=HTTP_201_CREATED)


class SuccessResponse(Response):
    def __init__(self, result=None):
        super().__init__(data=result, status=HTTP_200_OK)


class APIExceptionResponse(Response):
    def __init__(self, message=None, exception=None, status=HTTP_500_INTERNAL_SERVER_ERROR):
        message = message or 'An error occured.'
        code = status

        if exception is not None:
            message = str(exception)

        data = {'message': message, 'code': code}

        super().__init__(data=data, status=status)


class BadRequestException(APIExceptionResponse):
    def __init__(self, message=None, exception=None):
        super().__init__(message, exception, status=HTTP_400_BAD_REQUEST)


class UnauthorizedException(APIExceptionResponse):
    def __init__(self, message=None, exception=None):
        super().__init__(message, exception, status=HTTP_401_UNAUTHORIZED)


class ForbiddenException(APIExceptionResponse):
    def __init__(self, message=None, exception=None):
        super().__init__(message, exception, status=HTTP_403_FORBIDDEN)


class NotFoundException(APIExceptionResponse):
    def __init__(self, message=None, exception=None):
        super().__init__(message, exception, status=HTTP_404_NOT_FOUND)


class MethodNotAllowedException(APIExceptionResponse):
    def __init__(self, message=None, exception=None):
        super().__init__(message, exception, status=HTTP_405_METHOD_NOT_ALLOWED)


class InternalServerErrorException(APIExceptionResponse):
    def __init__(self, message=None, exception=None):
        super().__init__(message, exception)
