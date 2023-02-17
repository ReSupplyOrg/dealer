from django.core.cache import cache
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response

def Auth_Middleware(request):
    if 'session' in request.headers:
            session = request.headers["session"]
            uuid_v = cache.get(session)

            return uuid_v
