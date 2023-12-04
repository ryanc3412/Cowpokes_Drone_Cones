from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from drone_cones.models import Products, Drone, Account, Orders
from drone_cones.views import addDrone, addOrder
import json

class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.account = Account.objects.create(
            user=self.user,
            firstName='John',
            lastName='Doe',
            email='john.doe@example.com',
            address='123 Main St',
            city='Cityville',
            state='ST',
            zip='12345'
        )
        self.drone = Drone.objects.create(
            account=self.account,
            droneName='Test Drone',
            size='Large',
            scoops=10,
            isActive=True
        )
        self.product = Products.objects.create(
            type='Ice Cream',
            flavor='Vanilla',
            stockAvailable=100
        )

    def test_add_drone_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('drone_cones:add_drone'), {
            'drone_name': 'New Drone',
            'size': 'Medium',
            'scoops': 5
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue(Drone.objects.filter(droneName='New Drone').exists())

    def test_order_page_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('drone_cones:order'))
        self.assertEqual(response.status_code, 200)

    def test_drone_register_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('drone_cones:drone_register'))
        self.assertEqual(response.status_code, 200)  # Expecting a success response

    def test_edit_drone_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('drone_cones:edit_drone', args=[self.drone.id]), {
            'drone_name': 'Updated Drone',
            'drone_size': 'Small',
            'drone_capacity': 3,
            'is_active': False
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.drone.refresh_from_db()
        self.assertEqual(self.drone.droneName, 'Updated Drone')

    def test_admin_dash(self):
        self.client.force_login(self.user)
        self.account.is_admin = True
        self.account.save()

        response = self.client.get(reverse('drone_cones:admin_page'))

        self.assertEqual(response.status_code, 200)

        self.assertTrue('stock_list' in response.context)
        self.assertTrue('drone_list' in response.context)


class CreateAccountTestCase(TestCase):

    def test_create_account(self):
        username = 'testuser'
        password = 'testpassword'
        first_name = 'Test'
        last_name = 'User'
        email = 'test@example.com'

        response = self.client.post(reverse('drone_cones:create_account'), {
            'username': username,
            'password1': password,
            'password2': password,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        })

        self.assertEqual(response.status_code, 302)  # Redirect status code

        # Check if the user and associated account exist in the database
        self.assertTrue(User.objects.filter(username=username).exists())
        user = User.objects.get(username=username)
        self.assertTrue(Account.objects.filter(user=user, firstName=first_name, lastName=last_name, email=email).exists())

    def test_create_account_invalid_data(self):

        response = self.client.post(reverse('drone_cones:create_account'), {
            'username' : 1,
            'password1' : 2
        })


        self.assertNotEqual(response.status_code, 302)

        # Check if the user and associated account do not exist in the database
        self.assertFalse(User.objects.filter(username='invaliduser').exists())
        self.assertFalse(Account.objects.filter(user__username='invaliduser').exists())


class UserViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='Test',
            last_name='User',
            email='test@example.com',
        )
        self.account = Account.objects.create(
            user=self.user,
            firstName='Test',
            lastName='User',
            email='test@example.com',
        )

    def test_account_page(self):

        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('drone_cones:account'))

        self.assertEqual(response.status_code, 200)

    def test_edit_account(self):

        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('drone_cones:edit_account'), {
            'username': 'newusername',
            'first_name': 'NewFirst',
            'last_name': 'NewLast',
        })

        self.assertEqual(response.status_code, 302)

        # Check if the user and associated account were updated in the database
        self.user.refresh_from_db()
        self.account.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.account.firstName, 'NewFirst')
        self.assertEqual(self.account.lastName, 'NewLast')

    def test_edit_address(self):

        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('drone_cones:edit_address'), {
            'address_1': 'NewAddress1',
            'address_2': 'NewAddress2',
            'city': 'NewCity',
            'state': 'NewState',
            'zip': '12345',
        })

        self.assertEqual(response.status_code, 302)

        # Check if the user's address information was updated in the database
        self.account.refresh_from_db()
        self.assertEqual(self.account.address, 'NewAddress1')
        self.assertEqual(self.account.address2, 'NewAddress2')
        self.assertEqual(self.account.city, 'NewCity')
        self.assertEqual(self.account.state, 'NewState')
        self.assertEqual(self.account.zip, '12345')

class ManagerViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='Test',
            last_name='User',
            email='test@example.com',
        )
        self.account = Account.objects.create(
            user=self.user,
            firstName='Test',
            lastName='User',
            email='test@example.com',
            is_admin= True
        )

    def test_view_users(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('drone_cones:all_users'))
        self.assertEqual(response.status_code, 200)
    

    def test_view_stock(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('drone_cones:stock'))
        self.assertEqual(response.status_code, 200)
    

    def test_view_finances(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('drone_cones:finance'))
        self.assertEqual(response.status_code, 200)

    def test_view_drones(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('drone_cones:all_drones'))
        self.assertEqual(response.status_code, 200)


class OrderViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.account = Account.objects.create(
            user=self.user,
            firstName='Test',
            lastName='User',
            email='test@example.com',
            address='123 Test St',
            address2 = '123 Test St',
            city='Test City',
            state='TS',
            zip='12345'
        )

    def test_add_to_cart(self):

        self.client.force_login(self.user)

        data = json.dumps({'address': '123 test st', 'address2': '123 test st', 'city': 'test city', 'state': 'TS', 'zip': '12345'})
        response = self.client.post(reverse('drone_cones:add_to_cart'), data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.account.refresh_from_db()

        expected_value = [{'address': '123 test st', 'address2': '123 test st', 'city': 'test city', 'state': 'TS', 'zip': '12345'}]

        self.assertEqual(self.account.cart, expected_value)


    def test_send_order(self):
        self.client.login(username='testuser', password='testpassword')

        # Add an item to the cart
        cart_data = {
            'address': '123 test st',
            'address2': '123 test st',
            'city': 'test city',
            'state': 'TS',
            'zip': '12345'
        }
        self.client.post(reverse('drone_cones:add_to_cart'), json.dumps(cart_data), content_type='application/json')

        order_data = {
            'address': '456 Test St',
            'address2' : '456 Test St',
            'city': 'Test City',
            'state': 'TS',
            'zip': '54321',
        }

        response = self.client.post(reverse('drone_cones:send_order'), order_data)

        self.assertEqual(response.status_code, 302)  # Redirect status
        created_order_exists = Orders.objects.filter(user=self.user).exists()

        self.assertTrue(created_order_exists)

    def test_remove_from_order(self):
        self.client.force_login(self.user)
        self.account.cart = [{'flavor': 'Vanilla', 'quantity': 1}]
        self.account.save()

        response = self.client.post(reverse('drone_cones:remove_from_order'), data='1', content_type='application/json')
        self.account.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.account.cart, [])

    def test_get_account_address(self):

        self.client.force_login(self.user)

        response = self.client.get(reverse('drone_cones:get_account_address'))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'address1': '123 Test St',
            'address2': '123 Test St',
            'city': 'Test City',
            'state': 'TS',
            'zip': '12345'
        })
