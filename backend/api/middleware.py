from django.core.cache import cache

def Auth_Middleware(request):
    if 'session' in request.headers:
            session = request.headers["session"]
            uuid_v = cache.get(session)

            return uuid_v
