from django.contrib import admin
from .models import Account, Drone, Orders, Admins, Products

admin.site.register(Account)
admin.site.register(Drone)
admin.site.register(Orders)
admin.site.register(Admins)
admin.site.register(Products)

