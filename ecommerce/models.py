from django.db import models
from django.contrib.auth.models import User
from utils.model_abstracts import Model
from django_extensions.db.models import(
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel
)

class Item(TimeStampedModel,ActivatorModel,TitleSlugDescriptionModel,Model):
    
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural ='Items',
        ordering =["id"]


    def __str__(self):
        return self.title

    stock = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    

    def amount(self):
        amount = float(self.price)
        return amount
    
    """
    managing the stock
    """

    def manage_stock(self,qty):
        new_stock = self.stock - int(qty)
        self.stock = new_stock
        self.save()

    """
    checking the stock avalibality
    """

    def check_stock(self,qty):
        if int(qty) > self.stock:
            return False
        return True
    

    """
    before adding a items to the cart this funtion check avalibilty of the item stock 
    """
    def add_to_cart(self,user,qty):
        if self.check_stock(qty):
            cartItem = CartItem.objects.create(
                item = self,
                quantity =qty,
                user =user)
            self.manage_stock(qty)
            return cartItem
        else:
            return None

    """
    before checking-out of the cart check the avalability of the stock   
    """
    def place_order(self,user,qty):
        if self.check_stock(qty):
            order = Order.objects.create(
                item = self,
                quantity = qty,
                user=user)
            self.manage_stock(qty)
            return order
        else:
            return None
    
  

class Cart(TimeStampedModel, ActivatorModel, Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Cart owner

class CartItem(TimeStampedModel, ActivatorModel, Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Order(TimeStampedModel,ActivatorModel,Model):
    
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ["id"]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, null=True,blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}-{self.item.title}"
    