from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import status, permissions, generics, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404

from titles.permissions import IsAdminAdmin
from .models import User
from .serializers import (RegEmailSerializer,
                          RegUserSerializer,
                          UserSerializer
                          )


class APIRegEmail(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = RegEmailSerializer(data=request.data)
        if serializer.is_valid():
            code = get_random_string(length=6, allowed_chars='123456789')
            serializer.save(confirmation_code=code)
            address = self.request.data['email']
            send_mail('Код подтверждения для регистрации на YamDB',
                      f'Ваш код подтверждения - {code}, '
                      f'используйте его для получения токена',
                      'mailsender@yamdb.ru',
                      [address],
                      fail_silently=False,
                      )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIRegUser(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = RegUserSerializer(data=request.data)
        email_adr = self.request.data['email']
        if serializer.is_valid():
            try:
                user = get_object_or_404(User, email=email_adr)
                token = AccessToken().for_user(user)
                response = {'access': str(token)}
            except Exception:
                serializer.save(email=email_adr, username=email_adr,
                                role=User.USER)
                user = get_object_or_404(User, email=email_adr)
                token = AccessToken().for_user(user)
                response = {'token': str(token)}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIGetUsers(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = UserSerializer


class UserMeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminAdmin, ]
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'], url_path='me',
            permission_classes=(permissions.IsAuthenticated,))
    def get_patch(self, request):
        if request.method == 'GET':
            user = User.objects.get(username=request.user)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = self.request.user
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid() and (
                    'user' in user.role and user.is_staff is False):
                serializer.save(role=User.USER)
                response = 'Вы можете изменить любые данные, кроме роли'
                return Response((response, serializer.data),
                                status=status.HTTP_200_OK)
            elif serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
