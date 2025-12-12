import requests
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from users.serializers import OuathCodeSerializer
from django.utils import timezone
import os
User = get_user_model()
class GoogleLoginAPIView(CreateAPIView):
    serializer_class = OuathCodeSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        token_response = requests.post(
            url="https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                "redirect_uri": os.environ.get("GOOGLE_CLIENT_URI"),
                "grant_type": "authorization_code",
            }
        )
        print("CLIENT_ID:", os.environ.get("GOOGLE_CLIENT_ID"))
        print("CLIENT_SECRET:", os.environ.get("GOOGLE_CLIENT_SECRET"))
        print("CLIENT_URI:", os.environ.get("GOOGLE_CLIENT_URI"))
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            return Response({"error": "Invalid access token!"}, status=400)
        
        user_info = requests.get(
            url="https://www.googleapis.com/oauth2/v3/userinfo",
            params={"alt": "json"},
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()
        print(f"user_info {user_info}")
        email = user_info.get('email')
        if not email:
            return Response({"error": "Email not provided"}, status=400)
        first_name = user_info.get('given_name', '')
        last_name = user_info.get('family_name', '')
        user, created = User.objects.get_or_create(
            email=email,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.last_login = timezone.now()
        if created:
            user.registration_source = "google"
        user.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({"access_token": str(refresh.access_token),
                        "refresh_token": str(refresh)})