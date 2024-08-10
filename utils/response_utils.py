from rest_framework import status
from rest_framework.response import Response


class ResponseUtils:
    def create_response(self, data, status_code):
        return Response(data, status=status_code)

class SuccessResponse(ResponseUtils):
    def success(self, data=None):
        return self.create_response(data, status.HTTP_200_OK)

    def created(self, data=None):
        return self.create_response(data, status.HTTP_201_CREATED)

class ErrorResponse(ResponseUtils):
    def format_error(self, message=None, errors=None, exception=None):
        if message:
            return {'message': message, 'errors': errors or []}
        elif exception:
            return {'message': str(exception), 'errors': [exception]}
        else:
            return {'message': 'An error occurred', 'errors': errors or []}

    def bad_request_error(self, message=None, errors=None, exception=None):
        data = self.format_error(message, errors, exception)

        return self.create_response(data, status.HTTP_400_BAD_REQUEST)

    def unauthorized_error(self, message=None, errors=None, exception=None):
        data = self.format_error(message, errors, exception)

        return self.create_response(data, status.HTTP_401_UNAUTHORIZED)

    def forbidden_error(self, message=None, errors=None, exception=None):
        data = self.format_error(message, errors, exception)

        return self.create_response(data, status.HTTP_403_FORBIDDEN)

    def not_found_error(self, message=None, errors=None, exception=None):
        data = self.format_error(message, errors, exception)

        return self.create_response(data, status.HTTP_404_NOT_FOUND)

    def internal_server_error(self, message=None, errors=None, exception=None):
        data = self.format_error(message, errors, exception)

        return self.create_response(data, status.HTTP_500_INTERNAL_SERVER_ERROR)
