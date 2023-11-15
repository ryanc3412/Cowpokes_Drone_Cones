
from django.urls import path, include
from . import views

app_name = 'drone_cones'
urlpatterns = [
    # path('login/', views.LoginView.login, name='login'),
    path('home/', views.UserView.user_dash, name='home'),
    path('', views.UserView.user_dash, name='home'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('logout/', views.LoginView.redirect_view, name='redirect'),
    path('order/', views.OrderView.order_page, name='order'),
    path('drones/', views.DroneView.drone_dash, name='drones'),
    path('account/', views.UserView.account_page, name='account'),
    path('drone_register', views.DroneView.drone_register, name='drone_register'),
    path('create_account', views.LoginView.create_account, name='create_account'),
    path('order_confirmation', views.OrderView.order_confirmation, name='order_confirmation'),
    path("add_drone", views.addDrone, name="add_drone"),

    # path('admin/', views.adminPage, name='admin'),
]
