from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from .models import Menu
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from .serializer import MenuSerializer


class StandartPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class ProductViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    pagination_class = StandartPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title',)
    filterset_fields = ('category',)

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy '):
            return [IsAdminUser(),]
        return [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permissions_classes=[IsAuthenticated])
    def add_to_favorites(self, request, pk=None):
        product = self.get_object()
        user = request.user
        if user.favorite_products.filter(pk=product.pk).exists():
            return Response({'detail': 'Product is already in favorites.'}, status=400)
        user.favorite_products.add(product)
        return Response({'detail': 'Product added to favorites.'}, status=201)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_from_favorites(self, request, pk=None):
        product = self.get_object()
        user = request.user
        if not user.favorite_products.filter(pk=product.pk).exists():
            return Response({'detail': 'Product is not in favorites.'}, status=400)
        user.favorite_products.remove(product)
        return Response({'detail': 'Product removed from favorites.'}, status=204)







