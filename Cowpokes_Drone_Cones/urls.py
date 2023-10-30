from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('drone_cones/', include('drone_cones.urls'))
]
