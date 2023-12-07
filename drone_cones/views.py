from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed
from drone_cones.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models.signals import post_save
from drone_cones.core.forms import SignUpForm, OrderForm
from django.shortcuts import redirect
from datetime import date, datetime, timedelta
from drone_cones.core.forms import *
import json
from django.shortcuts import render
from drone_cones.models import Products, Drone
from django.utils import timezone
from random import randint


def addDrone(request):

    user = request.user
    account = Account.objects.get(user=user)


    if request.method == 'POST':
        
        form = DroneRegisterForm(request.POST)

        if form.is_valid():

            drone_name = form.cleaned_data.get('drone_name')
            drone_size = form.cleaned_data.get('drone_size')

            if drone_size == "Large":
                drone_scoops = 10

            elif drone_size == "Medium":
                drone_scoops = "7"

            elif drone_size == "Small":
                drone_scoops = "5"

            else:
                return HttpResponseNotAllowed()

            account.drone_set.create(droneName = drone_name, size = drone_size, scoops = drone_scoops, isActive = True, dateRegistered=date.today())

            response = redirect("drone_cones/drones/")

            return HttpResponseRedirect("drones")

def addOrder(request):
    user = request.user
    associated_account = Account.objects.get(user=user)

    context = {'form': OrderForm(), 'account': associated_account}

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            form.save()
            account_id = associated_account.Id
            address = form.cleaned_data['address']
            address2 = form.cleaned_data['address2']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip']

            # Get selected flavor from the JavaScript
            selected_flavor1 = request.POST.get('items', '')

            # Process the selected flavor as needed

            drone = form.cleaned_data['drone']

            # _______________________
            # | SELECTING DRONE      |
            # |----------------------|
            # |______________________|

            drone_set = Drone.objects.all()
            
            


            time_ordered = datetime.now()

            timeToDeliver = (datetime.min + timedelta(minutes=10)).time()

            timeDelivered = time_ordered + timedelta(minutes=10)


            # Save the order to the database
            order = Orders.objects.create(
                account_id = account_id,
                address=address,
                address2=address2,
                city=city,
                state=state,
                zip=zip_code,
                items=order,  # Store selected flavor in JSONField
                drone=drone,
                timeOrdered=time_ordered,
                timeDelivered = timeDelivered,
                timeToDeliver = timeToDeliver,
                # Add other fields as needed
            )

            order.save()


            return render(request, 'drone_cones/confirmation_page.html', context)
        else:
            return render(request, 'drone_cones/order_page.html', context)

    return render(request, 'drone_cones/order_page.html', context)

def droneRegister(request):    
    user = request.user
    associated_account = Account.objects.get(user=user)
    return render(request, "drone_cones/drone_register_page.html", {'account':associated_account})

class LoginView:
    def login(request):
        return render(request, 'drone_cones/login_page.html')

    def redirect_view(request):
        response = redirect('/dronecones/accounts/logout/')
        return response
        
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
                user_account = Account(user=user, firstName=firstname, lastName=lastname, email=email, is_admin = False)

                user_account.save()

                login(request, user=user)
                return redirect('/dronecones/home/')
        else:
            form = SignUpForm()
        return render(request, "drone_cones/create_account_page.html", {'form': form})

class UserView:
    @login_required
    def user_dash(request):
        user = request.user
        associated_account = Account.objects.get(user=user)

        flavor_list = Products.objects.order_by('-type')
        context = {
            'flavor_list': flavor_list,
            'account': associated_account,
        }
        return render(request, 'drone_cones/home_page.html', context)

    @login_required
    def account_page(request):
        user = request.user
        associated_account = Account.objects.get(user=user)
        date_joined = user.date_joined.strftime("%m/%d/%Y")	

        order_list = Orders.objects.filter(account_id=associated_account.Id)

        context = {
            'account': associated_account,
            'first_name':associated_account.firstName, 
            'last_name':associated_account.lastName,
            'username':user.username, 
            'date_joined':date_joined,
            'address_1': associated_account.address,
            'address_2': associated_account.address2,
            'city': associated_account.city,
            'state': associated_account.state,
            'zip': associated_account.zip,
            'orderList': order_list}
            
        return render (request, 'drone_cones/account_page.html', context)

    @login_required
    def edit_account(request):

        user = request.user
        associated_account = Account.objects.get(user=user)

        if request.method == 'POST':
            form = EditAccountForm(request.POST)
            if form.is_valid():

                user_name = form.cleaned_data.get('username')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')

                if user.username != user_name:
                   user.username = user_name
                   user.save()
                
                associated_account.firstName = first_name
                associated_account.lastName = last_name

                associated_account.save()

                return HttpResponseRedirect("../account")                
        else:
            date_joined = user.date_joined.strftime("%m/%d/%Y")

            context = {'first_name':associated_account.firstName, 'last_name':associated_account.lastName, 'username':user.username, 'date_joined':date_joined, 'account':associated_account}

            return render (request, 'drone_cones/edit_account.html', context)

    @login_required
    def edit_address(request):

        user = request.user
        associated_account = Account.objects.get(user=user)


        if request.method == 'POST':
            form = EditAddressForm(request.POST)
            if form.is_valid():
                address_1 = form.cleaned_data.get('address_1')
                address_2 = form.cleaned_data.get('address_2')
                city = form.cleaned_data.get('city')
                state = form.cleaned_data.get('state')
                zip = form.cleaned_data.get('zip')

                associated_account.address = address_1
                associated_account.address2 = address_2
                associated_account.city = city
                associated_account.state = state
                associated_account.zip = zip

                associated_account.save()                
 
                return HttpResponseRedirect("../account")

        else:
            context = {
                'account': associated_account,
                'address_1': associated_account.address,
                'address_2': associated_account.address2,
                'city': associated_account.city,
                'state': associated_account.state,
                'zip': associated_account.zip
            }
            return render(request, 'drone_cones/edit_address.html', context)
            
class DroneView:
    @login_required
    def drone_dash(request):
        user = request.user
        associated_account = Account.objects.get(user=user)
        drone_list = associated_account.drone_set.all()

        context = {
            'account': associated_account,
            'drone_list': drone_list,
        }
        return render(request, 'drone_cones/drone_page.html', context)

    @login_required
    def drone_register(request):
        user = request.user
        associated_account = Account.objects.get(user=user)
        context = {'account':associated_account}
        return render(request, "drone_cones/drone_register_page.html", context)

    @login_required
    def edit_drone(request, drone_id):

        user = request.user
        associated_account = Account.objects.get(user=user)

        drone = Drone.objects.get(id = int(drone_id))

        # if requested drone does not belong to signed in user, terminate
        if drone not in associated_account.drone_set.all():
           return HttpResponseForbidden()

        if request.method == 'POST':
            form = EditDroneForm(request.POST)
            if form.is_valid():
               
                drone_name = form.cleaned_data.get('drone_name')
                drone_size = form.cleaned_data.get('drone_size')
                is_active = form.cleaned_data.get('is_active')

                if drone_size == "Large":
                    drone.scoops = 10

                elif drone_size == "Medium":
                    drone.scoops = "7"

                elif drone_size == "Small":
                    drone.scoops = "5"

                else:
                    return HttpResponseNotAllowed()

                drone.droneName = drone_name
                drone.size = drone_size
                drone.isActive = is_active
               
                drone.save()

                return HttpResponseRedirect("../../drones")
        else:

            drone = Drone.objects.get(id = int(drone_id))
            context = {'drone_id': drone_id, 'name': drone.droneName, 'size': drone.size, 'capacity': drone.scoops, 'is_active': drone.isActive, 'account': associated_account}
            return render(request, "drone_cones/edit_drone_page.html", context)

class ManagerView:
    def manager_dash(request):
	
        user = request.user
        associated_account = Account.objects.get(user=user)

        if associated_account.is_admin:
            return render(request, "drone_cones/manager_home.html")
        else:
            return HttpResponseForbidden()

    def view_users(request):

        user = request.user
        associated_account = Account.objects.get(user=user)

        context = {'accounts': Account.objects.all()}

        if associated_account.is_admin:
            return render(request, "drone_cones/all_users.html", context)
        else:
            return HttpResponseForbidden()

    def edit_user(request, account_id):

        user = request.user
        associated_account = Account.objects.get(user=user)

        if associated_account.is_admin:

            toggled_account = Account.objects.get(Id = account_id)

            toggled_user = toggled_account.user  

            if request.method == 'POST':
                form = EditUserManagerForm(request.POST)
                if form.is_valid():
    		
                    username = form.cleaned_data.get('username')
                    first_name = form.cleaned_data.get('first_name')
                    last_name = form.cleaned_data.get('last_name')
                    is_manager = form.cleaned_data.get('is_manager')

                    toggled_user.username = username
                    toggled_account.firstName = first_name
                    toggled_account.lastName = last_name
                    toggled_account.is_admin = is_manager

                    toggled_account.save()

                    return HttpResponseRedirect("../")
                else:
                    return HttpResponseForbidden()

            context = {'account':Account.objects.get(Id=account_id), 'id':account_id, 'username':toggled_user.username}

            return render(request, "drone_cones/edit_user_manager.html", context)
        else:
            return HttpResponseForbidden()

    def view_stock(request):
        # Get data for stock and drones
        stock_list = reversed(Products.objects.order_by('-type'))

        # Get data for orders
        order_list = Orders.objects.all()

        context = {
            'stock_list': stock_list,
        }

        if associated_account.is_admin:
            return render(request, "drone_cones/stock_page.html")
        else:
            return HttpResponseForbidden()


    def edit_stock(request, product_id):
    # Retrieve the logged-in user and associated account
        user = request.user
        associated_account = Account.objects.get(user=user)

        # Retrieve the product based on the product_id
        product = Products.objects.get(id = product_id)
        current_stock = product.stockAvailable

        if request.method == 'POST':
            form = EditStock(request.POST)
            if form.is_valid():
                # Get the new stock value from the form
                add_stock = form.cleaned_data.get('stockAvailable')

                # Update the stockAvailable field of the product
                product.stockAvailable = add_stock + current_stock
                product.save()

                # Redirect to a success page or any other desired page
                return HttpResponseRedirect("../")

        else:
            return HttpResponseForbidden()

        context = {
            'form': form,
            'product': product,
        }

        return render(request, "drone_cones/edit_stock.html", context)





    def view_finances(request):

        user = request.user
        associated_account = Account.objects.get(user=user)

        # Get data for stock and drones
        stock_list = reversed(Products.objects.order_by('-type'))

        # Get data for orders
        order_list = Orders.objects.all()

        # Calculate total scoops, cones, and toppings
        total_scoops = sum(order['items']['scoops'] for order in order_list.values('items'))
        total_cones = sum(order['items']['cones'] for order in order_list.values('items'))
        total_toppings = sum(order['items']['toppings'] for order in order_list.values('items'))

        # Calculate total cost for each product type
        total_cost_ice_cream = sum(order['items']['cost'] for order in order_list.filter(items__type='Ice Cream').values('items'))
        total_cost_cone = sum(order['items']['cost'] for order in order_list.filter(items__type='Cone').values('items'))
        total_cost_topping = sum(order['items']['cost'] for order in order_list.filter(items__type='Topping').values('items'))

        #costs 
        total_revenue = total_cost_ice_cream + total_cost_cone + total_cost_topping
        drone_owner_payout = total_revenue * 0.1 #10% of revenue goes to drone owners
        inventory_cost = total_revenue * 0.2 #20% of income goes back to restocking inventories
        net_profit = total_revenue - drone_owner_payout - inventory_cost


        context = {
            'stock_list': stock_list,
            'total_scoops': total_scoops,
            'total_cones': total_cones,
            'total_toppings': total_toppings,
            'total_cost_ice_cream': total_cost_ice_cream,
            'total_cost_cone': total_cost_cone,
            'total_cost_topping': total_cost_topping,
            'total_revenue': total_revenue,
            'drone_owner_payout': drone_owner_payout,
            'inventory_cost': inventory_cost,
            'net_profit': net_profit,
        }

        if associated_account.is_admin:
            return render(request,  "drone_cones/stock_page.html")
        else:
            return HttpResponseForbidden()
 
    def view_drones(request):
        user = request.user
        associated_account = Account.objects.get(user=user)

        context = {'drones': Drone.objects.all()}

        if associated_account.is_admin:
            return render(request,  "drone_cones/all_drones.html", context)
        else:
            return HttpResponseForbidden()

    def edit_drone(request, drone_id):
        user = request.user
        associated_account = Account.objects.get(user=user)

        if associated_account.is_admin:

            drone = Drone.objects.get(id = drone_id)

            if request.method == 'POST':
                form = EditDroneForm(request.POST)
                if form.is_valid():

                    drone_name = form.cleaned_data.get('drone_name')
                    drone_size = form.cleaned_data.get('drone_size')
                    is_active = form.cleaned_data.get('is_active')
     
                    if drone_size == "Large":
                        drone.scoops = 10

                    elif drone_size == "Medium":
                        drone.scoops = "7"

                    elif drone_size == "Small":
                        drone.scoops = "5"

                    else:
                        return HttpResponseNotAllowed()

                    drone.droneName = drone_name
                    drone.size = drone_size
                    drone.isActive = is_active

                    drone.save()

                    return HttpResponseRedirect("../")
                else:
                    return HttpResponseForbidden()

            context = {'drone': Drone.objects.get(id=drone_id), 'drone_id':drone_id, 'account':drone.account, 'username':drone.account.user.username}

            return render(request, "drone_cones/edit_drone_manager.html", context)
        else:
            return HttpResponseForbidden()

class AdminView:
    @login_required
    def admin_dash(request):
        # Get data for stock and drones
        stock_list = reversed(Products.objects.order_by('-type'))

        # Get data for orders
        order_list = Orders.objects.all()

        # Calculate total scoops, cones, and toppings
        total_scoops = sum(order['items']['scoops'] for order in order_list.values('items'))
        total_cones = sum(order['items']['cones'] for order in order_list.values('items'))
        total_toppings = sum(order['items']['toppings'] for order in order_list.values('items'))

        # Calculate total cost for each product type
        total_cost_ice_cream = sum(order['items']['cost'] for order in order_list.filter(items__type='Ice Cream').values('items'))
        total_cost_cone = sum(order['items']['cost'] for order in order_list.filter(items__type='Cone').values('items'))
        total_cost_topping = sum(order['items']['cost'] for order in order_list.filter(items__type='Topping').values('items'))

        #costs 
        total_revenue = total_cost_ice_cream + total_cost_cone + total_cost_topping
        drone_owner_payout = total_revenue * 0.1 #10% of revenue goes to drone owners
        inventory_cost = total_revenue * 0.2 #20% of income goes back to restocking inventories
        net_profit = total_revenue - drone_owner_payout - inventory_cost


        context = {
            'stock_list': stock_list,
            'total_scoops': total_scoops,
            'total_cones': total_cones,
            'total_toppings': total_toppings,
            'total_cost_ice_cream': total_cost_ice_cream,
            'total_cost_cone': total_cost_cone,
            'total_cost_topping': total_cost_topping,
            'total_revenue': total_revenue,
            'drone_owner_payout': drone_owner_payout,
            'inventory_cost': inventory_cost,
            'net_profit': net_profit,
        }

        return render(request, 'drone_cones/admin_page.html', context)

class OrderView:
    @login_required
    def order_page(request):
        user = request.user
        associated_account = Account.objects.get(user=user)

        product_list = reversed(Products.objects.order_by("-id"))
        cart = Account.objects.get(user=request.user).cart

        context = {
            'product_list': product_list, 
            'cart': cart,
            'account': associated_account
        }

        return render(request, 'drone_cones/order_page.html', context)

    @login_required
    def order_confirmation(request):
        order = Orders.objects.first()
        context = {'order': order}
        return render(request, 'drone_cones/confirmation_page.html', context)

    def get_products(request):
        products = list(Products.objects.values())
        return JsonResponse(products, safe=False)

    def add_to_cart(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)

                user = request.user
                account = Account.objects.get(user=user)

                response = JsonResponse({'status': 'success'})
                redirect_url = '/dronecones/order/'
                response['X-Redirect'] = redirect_url

                ## if there is no cone ordered, we drone can't carry, thus we don't add to cart.
                if data == 'Invalid Order':
                    return response
                if account.cart is None:
                    account.cart = []
                    account.save()

                account.cart.append(data)
                account.save()

                return response
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)

    def send_order(request):
       
        if request.method == 'POST':
            form = OrderForm(request.POST)
            try: 
                user = request.user
                account = Account.objects.get(user=user)
                if (account.cart != []):
                    if (form.is_valid()):
                        address = form.cleaned_data['address']
                        address2 = form.cleaned_data['address2']
                        city = form.cleaned_data['city']
                        state = form.cleaned_data['state']
                        zip_code = form.cleaned_data['zip']

                        time_ordered = datetime.now()

                        time_to_deliver = (datetime.min + timedelta(minutes=10)).time()

                        time_delivered = time_ordered + timedelta(minutes=10)

                        eligible_drones = []
                        # filtering drone

                        print(f"There are {len(Drone.objects.all())} registered drones")
                        for drone in Drone.objects.all():
                            if (drone.scoops >= len(account.cart)) and (drone.isActive) and (not drone.isDelivering):
                                eligible_drones.append(drone)   
                       
                        print(f"There are {len(eligible_drones)} eligible drones") 
                        drone = eligible_drones[randint(0, len(eligible_drones)-1)]

                        Orders.objects.create(user=user, 
                                                account_id=account.Id, items=account.cart, 
                                                address=address,
                                                address2=address2,
                                                city=city,
                                                state=state,
                                                zip=zip_code,
                                                drone = drone.id,
                                                timeOrdered=time_ordered,
                                                timeDelivered= time_delivered,
                                                timeToDeliver= time_to_deliver)
                    else:
                        # Form is not valid, return form errors
                        return JsonResponse({'status': 'error', 'message': 'Invalid form data', 'errors': form.errors}, status=400)
                    ## empty cart
                    account.cart = []
                    account.save()
                    
                response = JsonResponse({'status': 'success'})
                redirect_url = '/dronecones/order/'
                response['X-Redirect'] = redirect_url

                return redirect(redirect_url)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)

    def remove_from_order(request):
        if request.method == 'POST':
            try:
                item_number = int(request.body)

                user = request.user
                account = Account.objects.get(user=user)
                if (len(account.cart) >= item_number):
                    account.cart.pop(item_number - 1)
                    account.save()

                redirect_url = '/dronecones/order/'

                response = JsonResponse({'status': 'success'})
                redirect_url = '/dronecones/order/'
                response['X-Redirect'] = redirect_url
                
                return response
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)

    def get_account_address(request):
        account = Account.objects.get(user=request.user)

        user_address_one = account.address
        user_address_two = account.address2
        user_city = account.city
        user_state = account.state
        user_zip = account.zip

        account_address_info = {'address1': user_address_one, 'address2': user_address_two, 'city': user_city, 'state': user_state, 'zip': user_zip}

        return JsonResponse(account_address_info, safe=False)
