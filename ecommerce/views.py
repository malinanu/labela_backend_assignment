from django.shortcuts import render
from json import JSONDecodeError
from django.http import JsonResponse
from .serializer import ItemSerializers,OrderSerializers,CartSerializer
from .models import Item,Order,Cart
from rest_framework import viewsets,status
from rest_framework.decorators import action 
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin,UpdateModelMixin,RetrieveModelMixin



class ItemViewSet(ListModelMixin,RetrieveModelMixin,viewsets.GenericViewSet
        ):

    """
    getting the items 

    """
    permission_classes = (IsAuthenticated,)
    quaryset =  Item.objects.all()
    serializer_class = ItemSerializers

class CartViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_cart(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        data = JSONParser().parse(request)
        try:
            item = Item.objects.get(pk=data['item_id'])
            cart = self.get_cart()
           
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
      

class OrderViewSet(ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        viewsets.GenericViewSet
        ):
    """
    getting and creating the orders

    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializers

    def get_queryset(self):
        user =self.request.user
        return Order.objects.filter(user=user)
    
    def create(self,requset):
        try:
            data = JSONParser().parse(requset)
            serializer = OrderSerializers(data=data)
            if serializer.is_valid(raise_exception=True):
                item = Item.objects.get(pk=data['item'])
                Order =Item.place_order(requset.user,data["quantity"])
                return Response(OrderSerializers(Order).data)
            else:
                return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decodeing"},status=400)