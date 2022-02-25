from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Categories, Products
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

    @staticmethod
    def _params_to_ints(qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve products for the authenticated user"""
        category = self.request.query_params.get('category')
        queryset = self.queryset

        if category:
            category_ids = self._params_to_ints(category)
            queryset = queryset.filter(category__id__in=category_ids)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.ProductDetailSerializer
        elif self.action == 'upload-image':
            pass
        return self.serializer_class
