import datetime, uuid
from django.core.mail import send_mail
from django.db.models import Q
from rest_framework import filters
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import User
from .permissions import Anonimous, IsAdmin
from .serializers import SignUpSerializer, AdminUserSerializer, UserSerializer


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAdmin,)

    def post(self, request):
        serializer = AdminUserSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(Q(username=request.data['username'])
                                   | Q(email=request.data['email'])).exists():
                raise Response(status=status.HTTP_400_BAD_REQUEST)
            user = self.get_object()
            user.save()
            return Response({'status': 'user created'})


class UserSignUp(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (Anonimous,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['post']

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get_or_create(
                username=request.data['username'],
                email=request.data['email'])
            user.confirmation_code = uuid.uuid4()
            user.key_expires = datetime.datetime.now + datetime.timedelta(days=1)
            send_mail("Your confirmation code",
                      str(user.confirmation_code),
                      None,
                      user.email,
                      fail_silently=False,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'patch']
