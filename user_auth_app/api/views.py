from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from user_auth_app.models import UserProfile


class Auth_View(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        action = request.data.get('action')

        if action == 'register':
            return self.register(request)
        elif action == 'login':
            return self.login(request)
        elif action == 'logout':
            return self.logout(request)
        else:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

    def register(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number', '')
        color = request.data.get('color', 'green')

        if not username or not email or not password:
            return Response(
                {"error": "Username, email, and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username, email=email, password=password)
        
        user.userprofile.phone_number = phone_number
        user.userprofile.color = color
        user.userprofile.save()

        # UserProfile.objects.create(
        #     user=user, phone_number=phone_number, color=color)

        # if not hasattr(user, 'userprofile'):
        #     UserProfile.objects.create(user=user)

        token = Token.objects.create(user=user)

        return Response({
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        user_profile = user.userprofile

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'email': user.email,
                'phone_number': user_profile.phone_number,
                'color': user_profile.color
            })
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    def logout(self, request):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        print(request.user)
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Token does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)

        user = request.user
        user.delete()

        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
