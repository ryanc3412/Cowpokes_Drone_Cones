from django.contrib import admin
# from django.urls import include, path


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('drone_cones/', include('drone_cones.urls'))
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dronecones/', include('drone_cones.urls')),
    # path('accounts/', include("django.contrib.auth.urls")),
]
