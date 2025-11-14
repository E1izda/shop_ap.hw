import random
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

confirmation_codes = {}

@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password or not email:
        return Response({'error': 'Заполните все поля'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Такой пользователь уже есть'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
    code = f"{random.randint(20, 30)}"
    confirmation_codes[email] = code

    return Response({'message': 'Пользователь создан. Подтвердите аккаунт кодом.', 'code': code}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def confirm_user_view(request):
    email = request.data.get('email')
    code = request.data.get('code')

    if not email or not code:
        return Response({'error': 'Укажите email и код'}, status=status.HTTP_400_BAD_REQUEST)

    if email not in confirmation_codes:
        return Response({'error': 'Код для этого email не найден'}, status=status.HTTP_400_BAD_REQUEST)

    if confirmation_codes[email] != code:
        return Response({'error': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        del confirmation_codes[email]
    except User.DoesNotExist:
        return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'message': 'Пользователь успешно подтвержден.'})

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Неверное имя пользователя или пароль'}, status=status.HTTP_401_UNAUTHORIZED)
    if not user.is_active:
        return Response({'error': 'Аккаунт не подтвержден'}, status=status.HTTP_403_FORBIDDEN)

    return Response({'message': f'Добро пожаловать, {user.username}!'})

