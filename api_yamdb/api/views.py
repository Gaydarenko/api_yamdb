from .permissions import IsAdminModeratorOwnerOrReadOnly
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .serializers import (CommentSerializer, ReviewSerializer, UsersSerializer,
                          GetTokenSerializer, CategorySerializer,
                          GenreSerializer, SignUpSerializer, TitleSerializer)
from rest_framework.decorators import action, api_view
from rest_framework import permissions, status, viewsets, pagination
from rest_framework import filters, mixins
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Review, User, Title, Category, Genre
from .permissions import IsAdminOrReadOnly, IsAdminModeratorOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    http_method_names = ('patch', 'post', 'get', 'delete')

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=(permissions.IsAuthenticated,), url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            user = request.user
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


@api_view(['POST'])
def api_get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, data['confirmation_code']):
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_201_CREATED)
    raise ValidationError('Invalid value')


@api_view(['POST'])
def api_signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    try:
        user, _ = User.objects.get_or_create(
            **serializer.validated_data
        )
    except Exception:
        return Response(
            'Такой username или e-mail уже используется.',
            status=status.HTTP_400_BAD_REQUEST)
    user, _ = User.objects.get_or_create(username=username, email=email)
    code = default_token_generator.make_token(user)
    message = f'Здравствуйте, {username}! Ваш код подтверждения: {code}'
    send_mail(_, message, 'support@yamdb.com', [email])
    return Response(serializer.data, status=status.HTTP_200_OK)


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
