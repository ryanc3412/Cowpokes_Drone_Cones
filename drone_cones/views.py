from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from drone_cones.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models.signals import post_save
from drone_cones.core.forms import SignUpForm, OrderForm
from django.shortcuts import redirect
from datetime import date
from drone_cones.core.forms import DroneRegisterForm

def addDrone(request):
    if request.method == 'POST':
        
        form = DroneRegisterForm(request.POST)
        print(f"FORM IS VALID: {form.is_valid()}")

        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print("boy howdy")

            form_drone_name = form.cleaned_data['drone_name']
            form_size = form.cleaned_data['size']
            form_scoops = form.cleaned_data['scoops']
          
            account = Account.objects.filter(pk = 1)[0]

            account.drone_set.create(droneName = form_drone_name, size = form_size, scoops = form_scoops, isActive = True, dateRegistered=date.today())

            response = redirect("drone_cones/drones/")

            return HttpResponseRedirect("drones")

def addOrder(request):
    if request.method == 'POST':
        
        form = OrderForm(request.POST)
        print(f"FORM IS VALID: {form.is_valid()}")

        if form.is_valid():

            form.save()

            form_items = form.clean_jsonfield['items']
            form_address = form.cleaned_data['address']
            form_address2 = form.cleaned_data['address2']
            form_city = form.cleaned_data['city']
            form_state = form.cleaned_data['state']
            form_zip = form.cleaned_data['zip']

            return redirect('/dronecones/confirmation_page.html')
        else:
            form = OrderForm()
        return render(request, "drone_cones/order_page.html")
	
def droneRegister(request):    
    return render(request, "drone_cones/drone_register_page.html")

class LoginView:
    def login(request):
        return render(request, 'drone_cones/login_page.html')

    def redirect_view(request):
        response = redirect('/dronecones/accounts/logout/')
        return response
        
    def create_user(request):
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():

                form.save()
                
                username = form.cleaned_data.get('username')
                firstname = form.cleaned_data.get('first_name')
                lastname = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                address = form.cleaned_data.get('address')
                address2 = form.cleaned_data.get('address2')
                city = form.cleaned_data.get('city')
                state = form.cleaned_data.get('state')
                zip = form.cleaned_data.get('zip')
                raw_password = form.cleaned_data.get('password1')

                
                user = authenticate(username=username, password=raw_password, firstname=firstname)
                login(request, user=user)
  
                # account = get_object_or_404(Account, username=username, firstName=firstname)

                # account.address = address

                return redirect('/dronecones/home/')
        else:
            form = SignUpForm()
        return render(request, "drone_cones/create_account_page.html", {'form': form})
    
    @receiver(post_save, sender=User)
    def account_create(sender, instance=None, created=False, **kwargs):
        if created:
            Account.objects.create(user=instance, lastName=User.last_name, firstName=User.first_name, email=User.email, username=User.username)

### don't start by inputing the address field... do that in the account page, and that way we can modify later with less security...

class UserView:
    def view_cart():
        pass

    def view_profile():
        pass

    @login_required
    def user_dash(request):
        flavor_list = Products.objects.order_by('-type')
        context = {
            'flavor_list': flavor_list,
        }
        return render(request, 'drone_cones/home_page.html', context)

    @login_required
    def account_page(request):
        return render (request, 'drone_cones/account_page.html', {})
    
class DroneView:
    @login_required
    def drone_dash(request):
        drone_list = Drone.objects.order_by('-droneName')
        context = {
            'drone_list': drone_list,
        }
        return render(request, 'drone_cones/drone_page.html', context)

    def view_drones():
        pass

    @login_required
    def drone_register(request):
        return render(request, "drone_cones/drone_register_page.html")

    def edit_drones():
        pass

class AdminView:
    def admin_dash():
        pass

    def view_users():
        pass

    def edit_users():
        pass

class OrderView:
    def order_view():
        pass

    @login_required
    def order_page(request):
        product_list = reversed(Products.objects.order_by("-id"))
        stock_list = reversed(Products.objects.order_by("-stockAvailable"))
        context = {'productList': product_list, 'stockAvailable': stock_list}
        return render(request, 'drone_cones/order_page.html', context)

    @login_required
    def order_confirmation(request):
        orders = reversed(Orders.objects.order_by("-id"))
        context = {'orders': orders}
        return render(request, 'drone_cones/confirmation_page.html', context)

    def edit_address():
        pass

    def add_address():
        pass
