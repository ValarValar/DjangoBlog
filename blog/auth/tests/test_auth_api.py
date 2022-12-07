from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class AuthEndpointsTestCase(APITestCase):
    def test_user_register_ok(self):
        user_1 = {
            'email': 'test@mail.ru',
            'password': '123qwer123!',
            'password2': '123qwer123!',
            'username': 'test_user',
        }
        url = reverse('auth_register')

        response = self.client.post(url, user_1)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        created_user_object = User.objects.get(username=user_1['username'])
        self.assertTrue(created_user_object)

    def test_user_login_ok(self):
        user_1 = {
            'username': 'test_user',
            'password': '123qwer123!',
        }
        url = reverse('token_obtain_pair')

        User.objects.create_user(**user_1)

        response = self.client.post(url, user_1)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        access = response.data.get('access')
        refresh = response.data.get('refresh')
        self.assertTrue(access)
        self.assertTrue(refresh)

    def test_user_register_unmatch_passwords(self):
        user_1 = {
            'email': 'test@mail.ru',
            'password': '1',
            'password2': '123qwer123!',
            'username': 'test_user',
        }
        url = reverse('auth_register')

        response = self.client.post(url, user_1)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_not_existing_user_login(self):
        user_1 = {
            'username': 'test_user',
            'password': '123qwer123!',
        }
        url = reverse('token_obtain_pair')

        response = self.client.post(url, user_1)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
