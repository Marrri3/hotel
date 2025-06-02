from django.contrib import admin
from products.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(characteristics)
admin.site.register(hotel_number)
admin.site.register(reservation)


