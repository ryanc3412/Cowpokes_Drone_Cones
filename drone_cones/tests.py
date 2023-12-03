from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from drone_cones.models import Products, Drone, Account, Orders
from unittest import mock
from drone_cones.views import addDrone, addOrder
from datetime import date

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

    def test_add_order_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('drone_cones:add_order'), {
            'user': self.user,
            'address': '456 Second St',
            'city': 'Townville',
            'state': 'TS',
            'zip': '67890',
            'drone': self.drone.id
        })
        self.assertEqual(response.status_code, 200)  # Expecting a success response
        self.assertTrue(Orders.objects.filter(address='456 Second St').exists()) #Expecting Database to be populated

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

        # Check if the account was created successfully
        self.assertEqual(response.status_code, 302)  # Redirect status code

        # Check if the user and associated account exist in the database
        self.assertTrue(User.objects.filter(username=username).exists())
        user = User.objects.get(username=username)
        self.assertTrue(Account.objects.filter(user=user, firstName=first_name, lastName=last_name, email=email).exists())

    def test_create_account_invalid_data(self):
        # Simulate a POST request with invalid data
        response = self.client.post(reverse('drone_cones:create_account'), {
            'username' : 1,
            'password1' : 2
        })

        # Check if the response is not a redirect
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

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

    def test_edit_account(self):

        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('drone_cones:edit_account'), {
            'username': 'newusername',
            'first_name': 'NewFirst',
            'last_name': 'NewLast',
        })

        # Check if the response is a redirect 
        self.assertEqual(response.status_code, 302)

        # Check if the user and associated account were updated in the database
        self.user.refresh_from_db()
        self.account.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.account.firstName, 'NewFirst')
        self.assertEqual(self.account.lastName, 'NewLast')

    def test_edit_address(self):

        self.client.login(username='testuser', password='testpassword')

        # Simulate a POST request to edit the address
        response = self.client.post(reverse('drone_cones:edit_address'), {
            'address_1': 'NewAddress1',
            'address_2': 'NewAddress2',
            'city': 'NewCity',
            'state': 'NewState',
            'zip': '12345',
        })

        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Check if the user's address information was updated in the database
        self.account.refresh_from_db()
        self.assertEqual(self.account.address, 'NewAddress1')
        self.assertEqual(self.account.address2, 'NewAddress2')
        self.assertEqual(self.account.city, 'NewCity')
        self.assertEqual(self.account.state, 'NewState')
        self.assertEqual(self.account.zip, '12345')
