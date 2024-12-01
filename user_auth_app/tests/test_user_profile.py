from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from user_auth_app.models import UserProfile

class UserProfileViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url_list = reverse('user-contacts')
        self.url_detail = reverse('user-contact-detail', args=[self.user.userprofile.id])

    def test_get_user_profiles(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_get_user_profile_detail(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['id'], self.user.id)

    def test_update_user_profile(self):
        data = {
            'phone_number': '9876543210',
            'color': 'red'
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['phone_number'], '9876543210')
        self.assertEqual(response.data['color'], 'red')

    def test_update_user_profile_partial(self):
        data = {
            'color': 'blue'
        }
        response = self.client.patch(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['color'], 'blue')

    def test_delete_user_profile(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(UserProfile.objects.filter(id=self.user.userprofile.id).exists())