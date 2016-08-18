from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.conf import settings

def custom_exception_handler(exc, context):
    """Return JSON 500 error responses."""
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
    else:
        if settings.DEBUG:
            detail = str(exc)
        else:
            detail = 'Internal Server Error'
        return Response(
            {'detail': detail},
            status=500
        )
    return response