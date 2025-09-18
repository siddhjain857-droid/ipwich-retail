import os
from django.http import JsonResponse


def healthz(request):
    return JsonResponse({"status": "ok", "commit": os.getenv("GIT_SHA", "dev")})