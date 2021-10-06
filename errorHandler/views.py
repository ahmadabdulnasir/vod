from rest_framework import status
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import get_object_or_404, render

RETURN_JSON = False

def error_400(request, exception, *args, **kwargs):
    template_name = "400.html"
    data = {"detail": "Bad Requests", "status_code": 400}
    status_code = status.HTTP_400_BAD_REQUEST
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)

def error_401(request, exception, *args, **kwargs):
    template_name = "error_handler/generic_error.html"
    data = {"detail": "Unauthorized", "status_code": 401}
    status_code = status.HTTP_401_UNAUTHORIZED
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)

def error_402(request, exception, *args, **kwargs):
    template_name = "error_handler/generic_error.html"
    data = {"detail": "Payment Required", "status_code": 402}
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)
     

def error_403(request, exception, *args, **kwargs):
    template_name = "403.html"
    data = {"detail": "Forbidden", "status": 403}
    status_code = status.HTTP_403_FORBIDDEN
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)


def error_404(request, exception, *args, **kwargs):
    template_name = "404.html"
    data = {"detail": "Not Found", "status": 404}
    status_code = status.HTTP_404_NOT_FOUND
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)


def error_405(request, exception, *args, **kwargs):
    template_name = "error_handler/generic_error.html"
    data = {"detail": "Request Method not Allowed", "status": 405}
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)


def error_406(request, exception, *args, **kwargs):
    template_name = "error_handler/generic_error.html"
    data = {"detail": "Request Method not Allowed", "status": 406}
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)


def error_413(request, exception, *args, **kwargs):
    template_name = "error_handler/generic_error.html"
    data = {"detail": "Request File too Large", "status": 413}
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)


def error_429(request, exception, *args, **kwargs):
    template_name = "error_handler/generic_error.html"
    data = {"detail": "Too Many Requests. Abort!!!", "status": 429}
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)

def error_431(request, exception, *args, **kwargs):
    template_name = "error_handler/generic_error.html"
    data = {"detail": "Request Header Fields Too Large. Abort!!!", "status": 431}
    status_code = status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)


def error_451(request, exception, *args, **kwargs):
    template_name = "error_handler/generic_error.html"
    data = {"detail": "Unavailable for Legal Reasons. Abort!!!", "status": 451}
    status_code = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)


def error_500(request, *args, **kwargs):
    template_name = "500.html"
    data = {"detail": "Internal Server Error", "status": 500}
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)


def error_501(request, exception, *args, **kwargs):
    template_name = "error_handler/generic_error.html"
    data = {"detail": "Not Implemented. Abort!!!", "status": 501}
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)

def error_502(request, exception, *args, **kwargs):
    template_name = "502.html"
    data = {"detail": "Bad Gateway!!!", "status": 502}
    status_code = status.HTTP_502_BAD_GATEWAY
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)


def error_503(request, exception, *args, **kwargs):
    template_name = "error_handler/generic_error.html"
    data = {"detail": "Service Unavailable. Abort!!!", "status": 503}
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)


def error_504(request, exception, *args, **kwargs):
    template_name = "error_handler/generic_error.html"
    data = {"detail": "Service Gateway Timeout. Abort!!!", "status": 504}
    status_code = status.HTTP_504_GATEWAY_TIMEOUT
    if RETURN_JSON:
        response = JsonResponse(data, status=status_code)
        response.status_code = status_code
        return response
    return render(request, template_name=template_name, context=data, status=status_code)

    
