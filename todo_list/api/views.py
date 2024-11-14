from todo_list.models import Subtask, Task, Contact
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import permissions, authentication

from django.contrib.auth import authenticate

from django.http import JsonResponse

from todo_list.models import Task
from todo_list.api.serializers import TaskItemSerializer, SubtaskSerializer
from user_auth_app.api.serializers import ContactSerializer
from rest_framework import generics


class AllTasks_View(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskItemSerializer


class SingleTask_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskItemSerializer

# class AllTasks_View(APIView):
#     # authentication_classes = [authentication.TokenAuthentication]
#     # permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, format=None):
#         tasks = Task.objects.all()
#         serializer = TaskItemSerializer(tasks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class SingleTask_View(APIView):
#     # authentication_classes = [authentication.TokenAuthentication]
#     # permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, format=None):
#         # return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         serializer = TaskItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             tasks = Task.objects.all()
#             all_tasks_serializer = TaskItemSerializer(tasks, many=True)
#             return Response(all_tasks_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, task_id, format=None):
#         try:
#             task = Task.objects.get(pk=task_id)
#             serializer = TaskItemSerializer(task)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Task.DoesNotExist:
#             return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, task_id, format=None):
#         try:
#             task = Task.objects.get(pk=task_id)
#         except Task.DoesNotExist:
#             return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = TaskItemSerializer(task, data=request.data, partial=True)
#         if serializer.is_valid():
#             updated_task = serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, task_id, format=None):
#         try:
#             task = Task.objects.get(pk=task_id)
#             task.delete()
#             tasks = Task.objects.all()
#             serializer = TaskItemSerializer(tasks, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Task.DoesNotExist:
#             return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)


class AllSubtasks_View(generics.ListAPIView):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer


class Subtask_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer


# class Subtask_View(APIView):

#     def post(self, request, task_id, format=None):
#         try:
#             task = Task.objects.get(pk=task_id)
#         except Task.DoesNotExist:
#             return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = SubtaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(task=task)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, subtask_id, format=None):
#         try:
#             subtask = Subtask.objects.get(pk=subtask_id)
#             serializer = SubtaskSerializer(subtask)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Task.DoesNotExist:
#             return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, subtask_id, format=None):
#         try:
#             subtask = Subtask.objects.get(pk=subtask_id)
#         except Subtask.DoesNotExist:
#             return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = SubtaskSerializer(
#             subtask, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, subtask_id, format=None):
#         try:
#             subtask = Subtask.objects.get(pk=subtask_id)
#             subtask.delete()
#             return Response({'deleted': True}, status=status.HTTP_204_NO_CONTENT)
#         except Subtask.DoesNotExist:
#             return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)


class All_Contacts_View(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class Contact_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
