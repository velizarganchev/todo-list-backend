from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from todo_list.models import Task
from todo_list.serializers import TaskItemSerializer


class Board_View(APIView):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskItemSerializer(tasks, many=True)

        return JsonResponse(serializer.data, safe=False)


class TaskItem_View(APIView):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        tasks = Task.objects.all()
        return Response(tasks)


class Login_View(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
