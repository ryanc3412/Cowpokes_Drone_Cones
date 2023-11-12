
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

    # path('account/', views.accountPage, name='account'),
    # path('order/', views.orderPage, name='order'),

### larnold ###

    # path("", views.homePage, name='home'),
    # path("home", views.homePage, name='home'),
    # path("order", views.orderPage, name="order"),
    # path("drones", views.dronePage, name="drones"),
    # path("account", views.accountPage, name="accounts"),
    # path("drone_register", views.droneRegister, name="drone_register"),
    # path("create_account", views.createAccount, name="create_account")

### end larnold ###

    # fill in here with urls
    # path("", views.homePage, name="home"),
    # path("home", views.homePage, name="home"),
    # path("order", views.orderPage, name="order"),
    # path("drones", views.dronePage, name="drones"),
    # path("account", views.accountPage, name="accounts"),

    #path('login/', views.loginPage, name='login'),
    # path('login/', views.loginPage, name='login'),
    # path('account/', views.accountPage, name='account'),
    # path('order/', views.orderPage, name='order'),

    # path('admin/', views.adminPage, name='admin'),
    # path('create_account/', views.createAccountPage, name='create_account'),
    # path('drones/', views.dronesPage, name='drones'),

    # path('drone_registration', views.droneRegistrationPage, name='drone_registration'),
]
