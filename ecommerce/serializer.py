from collections import OrderedDict
from .models import Item,Order,Cart,CartItem
from rest_framework_json_api import serializers
from rest_framework import status
from rest_framework.exceptions import APIException


class NotEnoughStockException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No stock"
    default_code='invalid'

class ItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'title',
            'stock',
            'price',
        )

class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializers(read_only=True)  

    class Meta:
        model = CartItem
        fields = ('id', 'item', 'quantity')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items') 


class OrderSerializers(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset = Item.objects.all(),many=False)
    class Meta:
        model = Order
        feilds = (
            'item',
            'quantity',
        )  

    def validate(self, res: OrderedDict):
        item = res.get('item')
        quantity = res.get('quantity')
        if not item.check_stock(quantity):
            raise NotEnoughStockException
        return res 