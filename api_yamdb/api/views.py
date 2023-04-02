from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer

from ..reviews.models import Category, Genre, Title


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
    # permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
    # permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('category__slug', 'genre__slug', 'name', 'year',)
    # permission_classes = (IsAdminOrReadOnly,)
