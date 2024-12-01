from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from todo_list.models import Task, Subtask
from rest_framework.authtoken.models import Token

class SubtaskTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@hotmai.com', password='testpassword')
        self.task = Task.objects.create(
            title='Test Task', description='Test Description', color='red')
        self.subtask = Subtask.objects.create(
            title='Test Subtask', status=False, task=self.task)
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_subtask(self):
        url = reverse('subtask-list')
        data = {
            'title': 'New Subtask',
            'status': False,
            'task': self.task.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_subtasks(self):
        url = reverse('subtask-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_subtask(self):
        url = reverse('subtask-detail', args=[self.subtask.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_subtask(self):
        url = reverse('subtask-detail', args=[self.subtask.id])
        data = {
            'title': 'Updated Subtask',
            'status': True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_subtask(self):
        url = reverse('subtask-detail', args=[self.subtask.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
