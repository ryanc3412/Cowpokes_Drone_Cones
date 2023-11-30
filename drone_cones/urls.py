
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
    path('drones/edit_drone/<int:drone_id>', views.DroneView.edit_drone, name='edit_drone'),
    path('account/', views.UserView.account_page, name='account'),
    path('edit_account/', views.UserView.edit_account, name='edit_account'),
    path('edit_address/', views.UserView.edit_address, name='edit_address'),
    path('drone_register', views.DroneView.drone_register, name='drone_register'),
    path('create_account', views.LoginView.create_account, name='create_account'),
    path('order_confirmation', views.OrderView.order_confirmation, name='order_confirmation'),
    path('admin_page', views.AdminView.admin_dash, name='admin_page'),
    path('add_drone', views.addDrone, name='add_drone'),
    path('add_order', views.addOrder, name='add_order'),
    path('manager/', views.ManagerView.manager_dash, name='manager'),
    path('manager/users/', views.ManagerView.view_users, name='all_users'),
    path('manager/finance/', views.ManagerView.view_finances, name='finance'),
    path('manager/stock/', views.ManagerView.view_stock, name='stock')
]
