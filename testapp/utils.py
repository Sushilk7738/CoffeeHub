from rest_framework.response import Response
from rest_framework import status


def api_success(payload = None, message = None, http_status = status.HTTP_200_OK):
    body = {}
    if message:
        body['message'] = message
    if payload:
        body.update(payload)
    return Response(body, status=http_status)


def api_error(message = "Something went wrong", http_status = status.HTTP_400_BAD_REQUEST, extra=None):
    body = {"error" : message}
    if extra and isinstance(extra, dict):
        body.update(extra)
    return Response(body, status=http_status)

    