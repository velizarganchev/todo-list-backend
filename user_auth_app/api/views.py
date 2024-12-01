from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from user_auth_app.models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer


class User_View(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number', '')
        color = request.data.get('color', 'green')

        if not username or not email or not password:
            return Response({'status': 'error', 'message': 'Username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'status': 'error', 'message': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.userprofile.phone_number = phone_number
        user.userprofile.color = color
        user.userprofile.save()

        token = Token.objects.create(user=user)
        return Response({'status': 'success', 'data': {
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'token': token.key
        }}, status=status.HTTP_201_CREATED)


class UserProfile_View(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, userprofile_id=None, format=None):
        if userprofile_id:
            try:
                userprofile = UserProfile.objects.get(pk=userprofile_id)
                serializer = UserProfileSerializer(userprofile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except UserProfile.DoesNotExist:
                return Response({'status': 'error', 'message': 'User Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            userprofiles = UserProfile.objects.all()
            serializer = UserProfileSerializer(userprofiles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, userprofile_id=None, format=None):
        try:
            userprofile = UserProfile.objects.get(pk=userprofile_id)
        except UserProfile.DoesNotExist:
            return Response({'status': 'error', 'message': 'User Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(
            userprofile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, userprofile_id=None, format=None):
        try:
            userprofile = UserProfile.objects.get(pk=userprofile_id)
        except UserProfile.DoesNotExist:
            return Response({'status': 'error', 'message': 'User Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(
            userprofile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        try:
            user.delete()
            return Response({'status': 'success', 'message': 'User and User Profile deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'status': 'error', 'message': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRegister_View(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name') or ''
        email = request.data.get('email')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number', '')
        color = request.data.get('color', 'green')

        if not username or not email or not password:
            return Response({'status': 'error', 'message': 'Username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'status': 'error', 'message': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'status': 'error', 'message': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.userprofile.phone_number = phone_number
        user.userprofile.color = color
        user.userprofile.save()

        token = Token.objects.create(user=user)
        user_profile = user.userprofile

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user_profile.phone_number,
            'color': user_profile.color
        }, status=status.HTTP_201_CREATED)


class UserLogin_View(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'status': 'error', 'message': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_exist = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'status': 'error', 'message': 'User with this email does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )

        user = authenticate(username=user_exist.username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            user_profile = user.userprofile
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_number': user_profile.phone_number,
                'color': user_profile.color
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'status': 'error', 'message': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class UserLogout_View(APIView):
    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'status': 'success', 'message': 'User logged out successfully.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'status': 'error', 'message': 'Token does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
