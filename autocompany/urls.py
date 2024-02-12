from django.contrib import admin
from django.urls import path
from ecommerce import views as ecom_views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()

router.register(r'item', ecom_views.ItemViewSet, basename='item')
router.register(r'order', ecom_views.OrderViewSet, basename='order')
router.register(r'cart', ecom_views.CartViewSet, basename='cart')


urlpatterns = router.urls


urlpatterns += [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token),
]
