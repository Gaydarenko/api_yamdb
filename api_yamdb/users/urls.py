from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import AdminUserViewSet, UserSignUp, UserViewSet


router = DefaultRouter()

router.register('auth/signup', UserSignUp)
router.register('users', AdminUserViewSet)
router.register('users/me', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
