from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register("categories", views.CategoriesViewSet)
router.register("products", views.ProductsViewSet)
router.register("orders", views.OrderViewSet)
router.register("items", views.OrderItemViewSet)

app_name = "api"  # pylint: disable=invalid-name

urlpatterns = [
    path("", include(router.urls)),
]
