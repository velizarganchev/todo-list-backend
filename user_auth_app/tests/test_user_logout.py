
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserLogoutViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user-logout')
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_logout_user_success(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User logged out successfully.')

    def test_logout_user_no_token(self):
        self.client.credentials()  # Remove token
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_logout_user_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalidtoken')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid token.')