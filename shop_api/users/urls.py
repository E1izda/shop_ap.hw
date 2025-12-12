from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.google_oauth import GoogleLoginAPIView

urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view()),
    path('confirm/', views.ConfirmUserAPIView.as_view()),
    path('login/', views.AuthorizationAPIView.as_view()),

    path('jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('google-login/', GoogleLoginAPIView.as_view()),

]
