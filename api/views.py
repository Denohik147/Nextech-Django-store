from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser, SAFE_METHODS

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from shop.models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


def clear_api_cache():
    cache.clear()


@method_decorator(cache_page(60 * 5), name='dispatch')
class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]

        return [IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save()
        clear_api_cache()


@method_decorator(cache_page(60 * 5), name='dispatch')
class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]

        return [IsAdminUser()]

    def perform_update(self, serializer):
        serializer.save()
        clear_api_cache()

    def perform_destroy(self, instance):
        instance.delete()
        clear_api_cache()


@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer

    filterset_fields = ['category']
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]

        return [IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save()
        clear_api_cache()


@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]

        return [IsAdminUser()]

    def perform_update(self, serializer):
        serializer.save()
        clear_api_cache()

    def perform_destroy(self, instance):
        instance.delete()
        clear_api_cache()