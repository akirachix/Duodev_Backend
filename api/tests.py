from django.test import TestCase, Client
from rest_framework.test import APIClient
from products.models import Products
from traders.models import Trader
from api.serializers import ProductsSerializer
from order.models import Order
from textilebale.models import TextileBale
from django.urls import reverse
from rest_framework import status
from users.models import User
from rest_framework.test import APITestCase
from footagent.models import FootAgent
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from traders.models import Trader
from django.utils import timezone
from datetime import timedelta
from products.models import Products
from footagent.models import FootAgent


User = get_user_model()

# Product Listing Tests --------(All Working)---------------------------------------------------------------
class ProductsListViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('products-list')  

        # Create a trader and a product for testing
        self.trader = Trader.objects.create_user(
        username='test_trader',
        password='test_password',
        first_name='John',
        last_name='Doe',
        phone_number='1234567890',
        number_of_posts=0  # Ensure this field is provided
        )
        self.product = Products.objects.create(
            product_name='Test Product',
            price=19.99,
            material='Cotton',
            description='A high-quality cotton product.',
            trader=None  # Assuming trader can be None
        )

    def test_list_products(self):
        response = self.client.get(self.list_url)
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data'], serializer.data)

    def test_create_product(self):
        data = {
            'product_name': 'New Product',
            'price': '29.99',
            'stock_quantity': 50,
            'material': 'Wool',
            'description': 'A new wool product.',
            'trader': None
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Products.objects.count(), 2)

    def test_create_product_invalid(self):
        data = {
            'product_name': '',  # Invalid data
            'price': 'invalid_price',
            'stock_quantity': -10,
            'material': '',
            'description': '',
            'trader': None
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.json())


# # Foot Agent Tests -----(All working)----------------------------------------------------------------------------------------


class FootAgentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.list_url = reverse('footagent-list')
        self.detail_url = lambda pk: reverse('footagent-detail', args=[pk])

    def test_create_foot_agent(self):
        data = {'agent_name': 'Agent One', 'location': 'Location One', 'user': self.user.pk}
        response = self.client.post(self.list_url, data, format='json')
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_foot_agent_invalid(self):
        data = {'agent_name': '', 'location': 'Location One', 'user': self.user.pk}
        response = self.client.post(self.list_url, data, format='json')
        print("Response data:", response.data)
        # Check if there are errors in the response data
        self.assertIn('agent_name', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_foot_agent(self):
        foot_agent = FootAgent.objects.create(user=self.user, agent_name='Agent One', location='Location One')
        data = {'agent_name': 'Updated Agent', 'location': 'Updated Location', 'user': self.user.pk}
        response = self.client.put(self.detail_url(foot_agent.pk), data, format='json')
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_foot_agent = FootAgent.objects.get(pk=foot_agent.pk)
        self.assertEqual(updated_foot_agent.agent_name, 'Updated Agent')
        self.assertEqual(updated_foot_agent.location, 'Updated Location')

    def test_list_foot_agents(self):
        FootAgent.objects.create(user=self.user, agent_name='Agent One', location='Location One')
        FootAgent.objects.create(user=self.user, agent_name='Agent Two', location='Location Two')
        response = self.client.get(self.list_url)
        print("Response data:", response.data)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_foot_agent(self):
        foot_agent = FootAgent.objects.create(user=self.user, agent_name='Agent One', location='Location One')
        response = self.client.get(self.detail_url(foot_agent.pk))
        print("Response data:", response.data)
        self.assertEqual(response.data['agent_name'], 'Agent One')

    def test_delete_foot_agent(self):
        foot_agent = FootAgent.objects.create(user=self.user, agent_name='Agent One', location='Location One')
        response = self.client.delete(self.detail_url(foot_agent.pk))
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



# # User Authentication Tests ------------------------------------------------------------------------

class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        self.login_url = '/api/token/' 

    def test_token_creation_on_login(self):
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(self.login_url, data, format='json')
# # User Registration Tests ------(All working)-----------------------------------------------------------------------------------
class UserRegistrationTests(APITestCase):
    def test_register_user(self):
        url = reverse('user-register')  # Ensure this matches the URL pattern name
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')

        # Print response for debugging
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.content.decode())




# Ordeer Tests --(All working)-------------------------------------------------------------------------------------------------

class OrderTests(APITestCase):
    def setUp(self):
        self.order_list_create_url = reverse('order-list-create')
        self.order_detail_url = lambda id: reverse('order-detail', args=[id])
        
        # Create a user for the order
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create a product for the order
        self.product = Products.objects.create(
            product_name='Sample Product',
            price=100.0,

            material='Cotton',
            description='A sample product description.'
        )
        
        # Create an order
        self.order = Order.objects.create(
            order_number='ORD001',
            phone_number='1234567890',
            product=self.product,
            user=self.user,
            quantity=1,
            total_price=100.0,
            location='Test Location'
        )

    def test_create_order(self):
        data = {
            'order_number': 'ORD002',
            'phone_number': '0987654321',
            'product': self.product.pk,
            'user': self.user.pk,
            'quantity': 2,
            'total_price': 200.0,
            'location': 'Another Location'
        }
        response = self.client.post(self.order_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.latest('id').order_number, 'ORD002')

    def test_retrieve_order(self):
        response = self.client.get(self.order_detail_url(self.order.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Use response.json() to access the response data
        response_data = response.json()
        self.assertIn('data', response_data)
        self.assertEqual(response_data['data']['order_number'], 'ORD001')
    def test_update_order(self):
        data = {
            'phone_number': '1122334455',
            'status': 'shipped'
        }
        response = self.client.put(self.order_detail_url(self.order.pk), data, format='json')
        print(response.data)  # Add this line to print the error details
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.phone_number, '1122334455')
        self.assertEqual(self.order.status, 'shipped')
        
    def test_delete_order(self):
            response = self.client.delete(self.order_detail_url(self.order.pk))
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Order.objects.count(), 0)
    



class TextileBaleTests(APITestCase):
    def setUp(self):
        """
        Set up initial data for the tests.
        """
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        
        # Adjust this to match the fields in the Trader model
        self.trader = Trader.objects.create(
            number_of_posts=0  # Include actual fields from Trader model
        )
        
        self.client.login(username='testuser', password='testpassword')

        # Create initial textile bale instance
        self.bale = TextileBale.objects.create(
            trader=self.trader,
            waste_type="Plastic",
            weight=100,
            price=50.00,
            posted_by=self.user
        )
    def test_create_textile_bale_with_image(self):
        url = reverse('textilebale-list')
        image_path = 'api/test_image.png'
        
        # Prepare the payload with image
        with open(image_path, 'rb') as image_file:
            data = {
                'trader': self.trader,
                'waste_type': 'Plastic',
                'weight': 100,
                'price': 50.00,
                'posted_by':1,  
                'image': image_file
            }
            response = self.client.post(url, data, format='multipart')


# Sales report  -----------------------------------------------------------------------------------------------

class SalesReportTests(APITestCase):
    def setUp(self):
        # Create products with the correct field names
        self.product1 = Products.objects.create(
            product_name='Product 1',
            price=100.00,
            material='Cotton',
            description='A high-quality cotton product'
        )
        self.product2 = Products.objects.create(
            product_name='Product 2',
            price=150.00,
            material='Wool',
            description='A premium wool product'
        )
    def create_orders(self):
        today = timezone.now()
        one_week_ago = today - timedelta(weeks=1)

        Order.objects.create(
            order_number='001',
            user=self.user,
            product=self.product1,
            order_date=today,
            quantity=10,
            total_price=self.product1.price * 10,
            location='Location 1',
            status='completed'
        )

        Order.objects.create(
            order_number='002',
            user=self.user,
            product=self.product2,
            order_date=today - timedelta(days=3),
            quantity=5,
            total_price=self.product2.price * 5,
            location='Location 2',
            status='completed'
        )

    def test_top_sold_product_of_week(self):
        url = reverse('top-sold-product-of-week')
        response = self.client.get(url)
    
        data = response.json()
        
    def test_total_sales(self):
        url = reverse('total-sales')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check if the total sales amount is correct
        total_sales = (self.product1.price * 10) + (self.product2.price * 5)


#Product Tessts ---------------------------------------------------------------------------------------
class ProductsTests(TestCase):
    def setUp(self):
        # Create a Trader instance
        self.trader = Trader.objects.create(
            username='test_trader',
            password='test_password',  # Assume password is handled properly
            number_of_posts=5
        )

        # Create Products instances
        self.product1 = Products.objects.create(
            product_name='Product 1',
            price=100.00,
            material='Cotton',
            description='A high-quality cotton product',
            trader=self.trader
        )
        self.product2 = Products.objects.create(
            product_name='Product 2',
            price=150.00,
            material='Wool',
            description='A premium wool product'
        )

    def test_product_creation(self):
        # Check if products were created correctly
        self.assertEqual(Products.objects.count(), 2)
        self.assertEqual(self.product1.product_name, 'Product 1')
        self.assertEqual(self.product2.price, 150.00)
        self.assertIsNone(self.product2.trader)

    def test_product_str(self):
        # Check the string representation of the product
        self.assertEqual(str(self.product1), 'Product 1')

    def test_product_trader_relationship(self):
        # Check if the product's trader is assigned correctly
        self.assertEqual(self.product1.trader, self.trader)
        self.assertIsNone(self.product2.trader)

    def test_update_product(self):
        # Update product details
        self.product1.product_name = 'Updated Product 1'
        self.product1.save()


    def test_delete_product(self):
        # Delete a product and check if it's removed
        self.product1.delete()
