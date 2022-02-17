from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('categories', views.CategoriesViewSet)
router.register('products', views.ProductsViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
