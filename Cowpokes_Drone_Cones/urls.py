
from django.contrib import admin
from django.urls import path

from drone_cones import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.login, name='login'),
    path('home/', views.UserView.user_dash, name='user_dash'),
]
