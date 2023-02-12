from django.contrib import admin

# Register your models here.
from .models import Stores, Clients, Packs, Orders, Ratings
admin.site.register(Stores)
admin.site.register(Clients)
admin.site.register(Packs)
admin.site.register(Orders)
admin.site.register(Ratings)