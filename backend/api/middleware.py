from django.core.cache import cache
from .models import Stores

def Auth_Middleware(request):
    if 'session' in request.headers:
            session = request.headers["session"]
            uuid_v = cache.get(session)

            return uuid_v

def Is_Store_Middleware(uuid):
    try:
        user = Stores.objects.get(uuid=uuid)
        return True
    except:
         return False
      