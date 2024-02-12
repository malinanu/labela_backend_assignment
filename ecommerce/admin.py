from django.contrib import admin
from . import models



@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id','title','price','stock','created', 'status')  # Added availability
    list_filter = ('status',)  # Filter for active/inactive items

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','item','quantity','user', 'created')
    list_filter = ('created',)  # Filter by order creation date

@admin.register(models.Cart)  # Assuming you created the Cart model 
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'modified')
    readonly_fields = ('modified',)  # Prevent manual edits


@admin.register(models.CartItem)  
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart','item' ,'quantity','created', 'modified')
    readonly_fields = ('modified',)  
