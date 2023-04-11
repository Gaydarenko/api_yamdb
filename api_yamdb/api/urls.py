from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, CommentViewSet, GenreViewSet,\
    ReviewViewSet, TitleViewSet, UsersViewSet, api_get_token, api_signup

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'users', UsersViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', api_signup, name='signup'),
    path('v1/auth/token/', api_get_token, name='get_token'),
]
