
from django.urls import path
from . import views

app_name = 'drone_cones'
urlpatterns = [

    # fill in here with urls

    path("", views.homePage, name="home"),
    path("home", views.homePage, name="home"),
    path("order", views.orderPage, name="order"),
    path("drones", views.dronePage, name="drones"),
    path("account", views.accountPage, name="accounts"),
    path("drone_register", views.droneRegister, name="drone_register"),
    path("create_account", views.createAccount, name="create_account"),
    path("order_confirmation", views.orderConfirmation, name="order_confirmation"),

    #path('login/', views.loginPage, name='login'),
    # path('account/', views.accountPage, name='account'),
    # path('order/', views.orderPage, name='order'),

    # path('admin/', views.adminPage, name='admin'),
    # path('create_account/', views.createAccountPage, name='create_account'),
    # path('drones/', views.dronesPage, name='drones'),

    # path('drone_registration', views.droneRegistrationPage, name='drone_registration'),
]
