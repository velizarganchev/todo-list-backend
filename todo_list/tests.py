from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from todo_list.models import Task
from rest_framework.authtoken.models import Token


class TaskTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@hotmai.com', password='testpassword')
        self.task = Task.objects.create(
            title='Test Task', description='Test Description', color='red')
        self.task.members.set([self.user.id])
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_task(self):
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'color': 'blue',
            "members": [
                self.user.id
            ],
            "subtasks": []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_task(self):
        url = reverse('task-detail', args=[self.task.id])
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'color': 'blue',
            "members": [
                self.user.id
            ],
            "subtasks": []
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_task_with_nested_fields(self):
        url = reverse('task-detail', args=[self.task.id])
        data = {
            'title': 'Updated Task with Nested Fields',
            'description': 'Updated Description',
            'color': 'green',
            "members": [
                self.user.id
            ],
            "subtasks": [
                {'title': 'Subtask 1', 'status': False},
                {'title': 'Subtask 2', 'status': True}
            ]
        }
        response = self.client.put(url, data, format='json')
        if response.status_code != 200:
            print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['subtasks']), 2)
        self.assertEqual(response.data['subtasks'][0]['title'], 'Subtask 1')
        self.assertEqual(response.data['subtasks'][1]['title'], 'Subtask 2')

    def test_delete_task(self):
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
