from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('categories', views.CategoriesViewSet)
router.register('products', views.ProductsViewSet)
router.register('orders', views.OrderViewSet)
router.register('order-items', views.OrderItemViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
