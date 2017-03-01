
from django.http import JsonResponse, HttpResponse


def bad_request(request):
    return _failure(404, "Url not valid")

def internal_error(request):
    return _failure(500, "BOOM! I don't know what it going on now!")

def _failure(code, message):
    failure = {"status_code" : code, "message" : message}
    return JsonResponse(failure)
