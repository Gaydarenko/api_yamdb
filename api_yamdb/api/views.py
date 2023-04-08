from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, pagination, viewsets

from reviews.models import Category, Comment, Genre, Review, Title, User

from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserSerializer)


class CategoryViewSet(viewsets.ModelViewSet, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, mixins.ListModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('category__slug', 'genre__slug', 'name', 'year',)
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    ...


class ReviewViewSet(viewsets.ModelViewSet):
    ...


class UserViewSet(viewsets.ModelViewSet):
    ...


class SignUp():
    ...


class GetToken:
    ...
