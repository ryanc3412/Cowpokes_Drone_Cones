from django.contrib import admin
from .models import *

admin.site.register(Account)
admin.site.register(Drone)
admin.site.register(Orders)
admin.site.register(Products)

