from todo_list.serializers import SubtaskSerializer
from todo_list.models import Subtask, Task
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import permissions, authentication

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.http import JsonResponse

from todo_list.models import Task
from todo_list.serializers import TaskItemSerializer


class AllTasks_View(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskItemSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleTask_View(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        # return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = TaskItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            tasks = Task.objects.all()
            all_tasks_serializer = TaskItemSerializer(tasks, many=True)
            return Response(all_tasks_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, task_id, format=None):
        try:
            task = Task.objects.get(pk=task_id)
            serializer = TaskItemSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, task_id, format=None):
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskItemSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            updated_task = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id, format=None):
        try:
            task = Task.objects.get(pk=task_id)
            task.delete()
            tasks = Task.objects.all()
            serializer = TaskItemSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)


class Subtask_View(APIView):

    def post(self, request, task_id, format=None):
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubtaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, subtask_id, format=None):
        try:
            subtask = Subtask.objects.get(pk=subtask_id)
            serializer = SubtaskSerializer(subtask)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, subtask_id, format=None):
        try:
            subtask = Subtask.objects.get(pk=subtask_id)
        except Subtask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubtaskSerializer(
            subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subtask_id, format=None):
        try:
            subtask = Subtask.objects.get(pk=subtask_id)
            subtask.delete()
            return Response({'deleted': True}, status=status.HTTP_204_NO_CONTENT)
        except Subtask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)


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

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
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
