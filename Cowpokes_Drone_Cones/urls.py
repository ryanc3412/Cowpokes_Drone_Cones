from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dronecones/', include('drone_cones.urls')),
    # path('accounts/', include("django.contrib.auth.urls")),
]
