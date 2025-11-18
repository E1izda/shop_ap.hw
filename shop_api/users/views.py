import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import ConfirmationCode
 
class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({'error': 'Заполните все поля'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Такой пользователь уже есть'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )

        code = str(random.randint(100000, 999999))
        ConfirmationCode.objects.create(user=user, code=code)

        return Response({'message': 'Пользователь создан', 'code': code},
                        status=status.HTTP_201_CREATED)


class ConfirmUserAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response({'error': 'Укажите email и код'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

        try:
            code_obj = ConfirmationCode.objects.get(user=user)
        except ConfirmationCode.DoesNotExist:
            return Response({'error': 'Код не найден'}, status=status.HTTP_400_BAD_REQUEST)

        if code_obj.code != code:
            return Response({'error': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        code_obj.delete()

        return Response({'message': 'Аккаунт подтвержден'})


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Неверное имя пользователя или пароль'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'error': 'Аккаунт не подтвержден'},
                            status=status.HTTP_403_FORBIDDEN)

        return Response({'message': f'Добро пожаловать, {user.username}!'})
