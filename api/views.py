from typing import Union, Any
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Categories, Products, Orders, OrderItem
from api import serializers


class CategoriesViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage Categories in the database"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Categories.objects.all()
    serializer_class = serializers.CategoriesSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    """Manage Products in the database"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Products.objects.all()
    serializer_class = serializers.ProductsSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        """Retrieve products for the authenticated user"""
        category = self.request.query_params.get("category")
        queryset = self.queryset

        if category:
            queryset = queryset.filter(category__name__in=[category.title()])

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == "retrieve":  # pylint: disable=no-else-return
            return serializers.ProductDetailSerializer
        elif self.action == "upload-image":
            pass
        return self.serializer_class


class OrderViewSet(viewsets.ModelViewSet):
    """Manage orders in the database"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Orders.objects.all()
    serializer_class = serializers.OrderSerializer

    @staticmethod
    def _params_to_ints(qs: list[str]) -> list[int]:
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve orders for the authenticated user"""
        order = self.request.query_params.get("order")
        queryset = self.queryset

        if order:
            order_ids = self._params_to_ints(order)
            queryset = queryset.filter(id__in=order_ids)

        return queryset.filter(user=self.request.user)

    @staticmethod
    def _calculate_total(
        price: Union[int, float], discount: float, quantity: int
    ) -> Union[int, float]:
        """helper function to calculate total price"""
        if discount is None or discount == 0:
            total_price = price * quantity
        else:
            total_price = (price - (price * discount / 100)) * quantity
        return total_price

    # pylint: disable=unused-argument
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create a new order"""
        order_total = []
        orders_data = request.data.pop("order_items")
        order = Orders.objects.create(user=request.user, **request.data)
        order.save()
        for order_data in orders_data:
            order_product_id = order_data.get("product")
            product = Products.objects.get(id=order_product_id)
            total_price = self._calculate_total(
                product.price, product.discount, order_data.get("quantity")
            )
            order_total.append(total_price)
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=order_data.get("quantity"),
                item_price=product.price,
                discount=product.discount,
                total_price=total_price,
            )
            order_item.save()
        order_total = sum(order_total)
        Orders.objects.filter(id=order.id).update(order_total=order_total)
        return Response(
            {"message": "Order created successfully."}, status.HTTP_201_CREATED
        )


class OrderItemViewSet(viewsets.ModelViewSet):
    """Manage order items for a specific order"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer

    @staticmethod
    def _params_to_ints(qs: list[str]) -> list[int]:
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve order items for the authenticated user"""
        order_item = self.request.query_params.get("order")
        queryset = self.queryset

        if order_item:
            order_item_ids = self._params_to_ints(order_item)
            queryset = queryset.filter(order_id__in=order_item_ids)

        return queryset.filter(order__user=self.request.user)
