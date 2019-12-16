import base64
from http import HTTPStatus
from django.test import TestCase
from rest_framework.test import APIClient


CLIENT = APIClient()


class Account(TestCase):
    def test_valid_account_can_be_created(self):
        email = "test@tester.com"
        password = "123456"
        data = {
            "email": email,
            "password": password
        }
        request = CLIENT.post('/accounts/create/', data=data, format='json')
        self.assertEqual(request.status_code, HTTPStatus.CREATED)
        self.assertIn('access', request.data)
        self.assertIn('refresh', request.data)

    def test_account_cannot_be_created_twice(self):
        email = "test2@tester.com"
        password = "123456"
        data = {
            "email": email,
            "password": password
        }
        request = CLIENT.post('/accounts/create/', data=data, format='json')
        self.assertEqual(request.status_code, HTTPStatus.CREATED)
        self.assertIn('access', request.data)
        self.assertIn('refresh', request.data)
        request = CLIENT.post('/accounts/create/', data=data, format='json')
        self.assertEqual(request.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn('error', request.data)
        self.assertEqual(request.data['error'], f"User with email {email} already exists")

    def test_user_can_login(self):
        email = "test3@tester.com"
        password = "123456"
        data = {
            "email": email,
            "password": password
        }
        request = CLIENT.post('/accounts/create/', data=data, format='json')
        self.assertEqual(request.status_code, HTTPStatus.CREATED)
        self.assertIn('access', request.data)
        self.assertIn('refresh', request.data)
        CLIENT.credentials(
            HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{email}:{password}'.encode()).decode()}"
        )
        request = CLIENT.post('/accounts/login/')
        self.assertEqual(request.status_code, HTTPStatus.OK)
        self.assertIn('access', request.data)
        self.assertIn('refresh', request.data)
        CLIENT.credentials()

    def test_non_existing_user_cannot_login(self):
        email = "nonexisting@tester.com"
        password = "123456"
        CLIENT.credentials(
            HTTP_AUTHORIZATION=f"Basic {base64.b64encode(f'{email}:{password}'.encode()).decode()}"
        )
        request = CLIENT.post('/accounts/login/')
        self.assertEqual(request.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertIn('detail', request.data)
        self.assertEqual(request.data['detail'], 'Invalid username/password.')
        CLIENT.credentials()

    def test_user_can_refresh_token(self):
        email = "test4@tester.com"
        password = "123456"
        data = {
            "email": email,
            "password": password
        }
        request = CLIENT.post('/accounts/create/', data=data, format='json')
        self.assertEqual(request.status_code, HTTPStatus.CREATED)
        self.assertIn('access', request.data)
        self.assertIn('refresh', request.data)
        data = {
            "refresh": request.data['refresh']
        }
        request = CLIENT.post('/accounts/tokenrefresh/', data=data, format='json')
        self.assertEqual(request.status_code, HTTPStatus.OK)
        self.assertIn('access', request.data)

    def test_non_existing_user_cannot_refresh_token(self):
        data = {
            "refresh": "a_token_that_does_not_exist"
        }
        request = CLIENT.post('/accounts/tokenrefresh/', data=data, format='json')
        self.assertEqual(request.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertIn('detail', request.data)
        self.assertIn('code', request.data)
        self.assertEqual(request.data['detail'], 'Token is invalid or expired')
        self.assertEqual(request.data['code'], 'token_not_valid')
