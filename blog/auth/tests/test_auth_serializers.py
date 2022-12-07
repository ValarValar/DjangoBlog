from django.contrib.auth.models import User
from django.test import TestCase

from auth.serializers import RegisterSerializer, MyTokenObtainPairSerializer


class RegisterSerializerTestCase(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass


    def test_output_data(self):
        user_1 = {
            'email': 'test@mail.ru',
            'password': '123qwer123!',
            'password2': '123qwer123!',
            'username': 'test_user',
        }

        serializer = RegisterSerializer(user_1)

        expected_data = {"username": "test_user", "email": "test@mail.ru"}
        data = serializer.data
        self.assertEqual(data, expected_data)

    def test_passwords_similarity_validation(self):
        user_1 = {
            'email': 'test@mail.ru',
            'password': '123qwer123!',
            'password2': '123qwer123!1',
            'username': 'test_user',
        }
        serializer = RegisterSerializer(data=user_1)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors.keys(), set(['password']))

    def test_username_email_validation(self):
        user_1 = {
            'password': '123qwer123!',
            'password2': '123qwer123!1',
        }
        serializer = RegisterSerializer(data=user_1)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors.keys(), set(['username', 'email']))




