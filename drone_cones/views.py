from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from drone_cones.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.forms import UserCreationForm
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models.signals import post_save
from drone_cones.core.forms import SignUpForm, OrderForm
from django.shortcuts import redirect
from datetime import date
from drone_cones.core.forms import DroneRegisterForm, EditAccountForm, EditAddressForm

from django.shortcuts import render
from drone_cones.models import Products, Drone

def addDrone(request):
    if request.method == 'POST':
        
        form = DroneRegisterForm(request.POST)
        print(f"FORM IS VALID: {form.is_valid()}")

        if form.is_valid():
            #form.save()

            form_drone_name = form.cleaned_data['drone_name']
            form_size = form.cleaned_data['size']
            form_scoops = form.cleaned_data['scoops']
         
            user = request.user 
            account = Account.objects.get(user=user)

            account.drone_set.create(droneName = form_drone_name, size = form_size, scoops = form_scoops, isActive = True, dateRegistered=date.today())

            response = redirect("drone_cones/drones/")

            return HttpResponseRedirect("drones")

def addOrder(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            # Process other form fields
            address = form.cleaned_data['address']
            address2 = form.cleaned_data['address2']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip']

            # Get selected flavor from the JavaScript
            selected_flavor = request.POST.get('selected_flavor', '')

            # Process the selected flavor as needed

            # Save the order to the database
            order = Orders.objects.create(
                address=address,
                address2=address2,
                city=city,
                state=state,
                zip=zip_code,
                items={'flavor': selected_flavor},  # Store selected flavor in JSONField
                # Add other fields as needed
            )

            return JsonResponse({'message': 'Order added successfully'})
        else:
            return JsonResponse({'error': 'Form is not valid'}, status=400)

    return render(request, 'drone_cones/order_page.html', {'form': OrderForm()})




	
def droneRegister(request):    
    return render(request, "drone_cones/drone_register_page.html")

class LoginView:
    def login(request):
        return render(request, 'drone_cones/login_page.html')

    def register(first_name, last_name, email, password):
        user = User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect_to_login('URL_GOES_HERE', 'LOGIN_URL')
    
    def redirect_view(request):
        response = redirect('/dronecones/accounts/logout/')
        return response
        
    def logout():
        pass

    # @receiver(post_save, sender=User)
    def create_account(request):
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                firstname = form.cleaned_data.get('first_name')
                lastname = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                user = authenticate(username=username, password=raw_password)
                user_account = Account(user=user, firstName=firstname, lastName=lastname, email=email)

                user_account.save()

                login(request, user=user)
                return redirect('/dronecones/home/')
        else:
            form = SignUpForm()
        return render(request, "drone_cones/create_account_page.html", {'form': form})

class UserView:
    def view_cart():
        pass

    def view_profile():
        pass

    #@login_required
    def user_dash(request):
        flavor_list = Products.objects.order_by('-type')
        context = {
            'flavor_list': flavor_list,
        }
        return render(request, 'drone_cones/home_page.html', context)

    #@login_required
    def account_page(request):
        user = request.user
        user_account = Account.objects.get(user=user)
        date_joined = user.date_joined.strftime("%m/%d/%Y")	

        context = {
            'first_name':user_account.firstName, 
            'last_name':user_account.lastName,
            'username':user.username, 
            'date_joined':date_joined,
            'address_1': user_account.address,
            'address_2': user_account.address2,
            'city': user_account.city,
            'state': user_account.state,
            'zip': user_account.zip}
        return render (request, 'drone_cones/account_page.html', context)

    @login_required
    def edit_account(request):

        if request.method == 'POST':
            form = EditAccountForm(request.POST)
            if form.is_valid():

                user_name = form.cleaned_data.get('username')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                
                user = request.user
                associated_account = Account.objects.get(user=user)

                if user.username != user_name:
                   user.username = user_name
                   user.save()
                
                associated_account.firstName = first_name
                associated_account.lastName = last_name

                associated_account.save()

                return HttpResponseRedirect("../account")                
        else:
            user = request.user
            user_account = Account.objects.get(user=user)
            date_joined = user.date_joined.strftime("%m/%d/%Y")

            context = {'first_name':user_account.firstName, 'last_name':user_account.lastName, 'username':user.username, 'date_joined':date_joined}
            return render (request, 'drone_cones/edit_account.html', context)
    @login_required
    def edit_address(request):

        user = request.user
        user_account = Account.objects.get(user=user)


        if request.method == 'POST':
            form = EditAddressForm(request.POST)
            if form.is_valid():
                address_1 = form.cleaned_data.get('address_1')
                address_2 = form.cleaned_data.get('address_2')
                city = form.cleaned_data.get('city')
                state = form.cleaned_data.get('state')
                zip = form.cleaned_data.get('zip')

                user_account.address = address_1
                user_account.address2 = address_2
                user_account.city = city
                user_account.state = state
                user_account.zip = zip

                user_account.save()                
 
                return HttpResponseRedirect("../account")

        else:
            context = {
                'address_1': user_account.address,
                'address_2': user_account.address2,
                'city': user_account.city,
                'state': user_account.state,
                'zip': user_account.zip
            }
            return render(request, 'drone_cones/edit_address.html', context)
            
    
class DroneView:
    #@login_required
    def drone_dash(request):
        user = request.user
        associated_account = Account.objects.get(user=user)
        drone_list = associated_account.drone_set.all()

        context = {
            'drone_list': drone_list,
        }
        return render(request, 'drone_cones/drone_page.html', context)

    def view_drones():
        pass

    #@login_required
    def drone_register(request):
        return render(request, "drone_cones/drone_register_page.html")

    @login_required
    def edit_drone(request, drone_id):
        drone = Drone.objects.get(id = int(drone_id))
        print(f"Drone name is {drone.droneName}")
        context = {'drone_id': drone_id, 'name': drone.droneName, 'size': drone.size, 'capacity': drone.scoops}
        return render(request, "drone_cones/edit_drone_page.html", context)

class AdminView:
    #@login_required
    def admin_dash(request):
        # Get data for stock and drones
        stock_list = Products.objects.order_by('-stockAvailable')
        drone_list = Drone.objects.order_by('-droneName')

        context = {
            'stock_list': stock_list,
            'drone_list': drone_list,
        }

        return render(request, 'drone_cones/admin_page.html', context)

# class AdminView:
#     def admin_dash():
#         pass

#     def view_users():
#         pass

#     def edit_users():
#         pass

class OrderView:
    def order_view():
        pass

    #@login_required
    def order_page(request):
        product_list = reversed(Products.objects.order_by("-id"))
        stock_list = reversed(Products.objects.order_by("-stockAvailable"))
        context = {'productList': product_list, 'stockAvailable': stock_list}
        return render(request, 'drone_cones/order_page.html', context)

    #@login_required
    def order_confirmation(request):
        orders = reversed(Orders.objects.order_by("-id"))
        context = {'orders': orders}
        return render(request, 'drone_cones/confirmation_page.html', context)

    def edit_address():
        pass

    def add_address():
        pass
