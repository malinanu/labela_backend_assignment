from django.contrib.auth.models import User
from ecommerce.models import Item, Order
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

class EcommerceTestCase(APITestCase):
    """
    Test suite for Items and Orders
    """
    def setUp(self):
        
        Item.objects.create(title="item 1", description="description for item 1", price=600, stock=25)
        Item.objects.create(title="item 2", description="description for item 2", price=800, stock=10)
        Item.objects.create(title="item 3", description="description for item 3", price=350, stock=20)
        Item.objects.create(title="item 4", description="description for item 4", price=450, stock=12)
        Item.objects.create(title="item 5", description="description for item 5", price=550, stock=35)
        Item.objects.create(title="item 6", description="description for item 6", price=600, stock=1)
        Item.objects.create(title="item 7", description="description for item 7", price=100, stock=2)
        self.items = Item.objects.all()
        self.user = User.objects.create_user(
            username='testUser',  
            password='dfsffs3243',  
            email='testusergmail@test.com'  
        )

    #     # Creating orders with the updated user and items
        Order.objects.create(item=Item.objects.first(), user=self.user, quantity=1)
        Order.objects.create(item=Item.objects.first(), user=self.user, quantity=2)

    #     # The app uses token authentication
        self.token = Token.objects.create(user=self.user)  # Ensure token is created if not already
        self.client = APIClient()

        # We pass the token in all calls to the API
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_all_items(self):
        '''
        test ItemsViewSet list method
        '''
        self.assertEqual(self.items.count(), 5)
        response = self.client.get('/item/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_item(self):
        '''
        test ItemsViewSet retrieve method
        '''
        for item in self.items:
            response = self.client.get(f'/item/{item.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_is_more_than_stock(self):
        '''
        test Item.check_stock when order.quantity > item.stock
        '''
        for i in self.items:
            current_stock = i.stock
            self.assertEqual(i.check_stock(current_stock + 1), False)

    def test_order_equals_stock(self):
        '''
        test Item.check_stock when order.quantity == item.stock
        '''
        for i in self.items:
            current_stock = i.stock
            self.assertEqual(i.check_stock(current_stock), True)

    def test_order_is_less_than_stock(self):
        '''
        test Item.check_stock when order.quantity < item.stock
        '''
        for i in self.items:
            current_stock = i.stock
            self.assertTrue(i.check_stock(current_stock - 1))

    def test_create_order_with_more_than_stock(self):
        '''
        test OrdersViewSet create method when order.quantity > item.stock
        '''
        for i in self.items:
            stock = i.stock
            data = {"item": str(i.id), "quantity": str(stock + 1)}
            response = self.client.post('/order/', data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_less_than_stock(self):
        '''
        test OrdersViewSet create method when order.quantity < item.stock
        '''
        for i in self.items:
            data = {"item": str(i.id), "quantity": 1}
            response = self.client.post('/order/', data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order_with_equal_stock(self):
        '''
        test OrdersViewSet create method when order.quantity == item.stock
        '''
        for i in self.items:
            stock = i.stock
            data = {"item": str(i.id), "quantity": str(stock)}
            response = self.client.post('/order/', data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_orders(self):
        '''
        test OrdersViewSet list method
        '''
        self.assertEqual(Order.objects.count(), 2)
        response = self.client.get('/order/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_order(self):
        '''
        test OrdersViewSet retrieve method
        '''
        orders = Order.objects.filter(user=self.user)
        for o in orders:
            response = self.client.get(f'/order/{o.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
