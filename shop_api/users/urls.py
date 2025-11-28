from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view()),
    path('confirm/', views.ConfirmUserAPIView.as_view()),
    path('login/', views.AuthorizationAPIView.as_view()),
]
