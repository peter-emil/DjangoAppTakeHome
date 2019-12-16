from http import HTTPStatus
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class UserFactory:
    @staticmethod
    def get_user(email: str, password: str = "123456") -> User:
        user, created = User.objects.get_or_create(
            email=email,
            username=email,
        )
        if created:
            user.set_password(password)
        return user


CLIENT = APIClient()
USER_FACTORY = UserFactory()


class MetadataTests(TestCase):
    def test_user_can_create_metadata(self):
        user = USER_FACTORY.get_user(email="metadata1@tester.com")
        CLIENT.force_authenticate(user=user)
        name = "metadata1"
        string = "this is a string"
        data = {
            "name": name,
            "string": string
        }
        request = CLIENT.post('/assets/metadata/', data=data, format='json')
        self.assertEqual(request.status_code, HTTPStatus.CREATED)
        self.assertIn('id', request.data)
        self.assertIn('name', request.data)
        self.assertIn('string', request.data)
        self.assertIn('owner', request.data)
        self.assertEqual(request.data['name'], name)
        self.assertEqual(request.data['string'], string)
        self.assertEqual(request.data['owner'], user.pk)
        CLIENT.force_authenticate(user=None)

    def test_user_cannot_deplicate_metadata_name(self):
        user = USER_FACTORY.get_user(email="metadata2@tester.com")
        CLIENT.force_authenticate(user=user)
        name = "metadata2"
        string = "this is a string"
        data = {
            "name": name,
            "string": string
        }
        request = CLIENT.post('/assets/metadata/', data=data, format='json')
        self.assertEqual(request.status_code, HTTPStatus.CREATED)
        self.assertIn('id', request.data)
        self.assertIn('name', request.data)
        self.assertIn('string', request.data)
        self.assertIn('owner', request.data)
        self.assertEqual(request.data['name'], name)
        self.assertEqual(request.data['string'], string)
        self.assertEqual(request.data['owner'], user.pk)
        request = CLIENT.post('/assets/metadata/', data=data, format='json')
        self.assertEqual(request.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn('name', request.data)
        self.assertIsInstance(request.data['name'], list)
        self.assertEqual(len(request.data['name']), 1)
        self.assertEqual(request.data['name'][0], "metadata entry with this name already exists.")
        CLIENT.force_authenticate(user=None)

    def test_unauthenticated_user_cannot_create_metadata(self):
        name = "metadata3"
        string = "this is a string"
        data = {
            "name": name,
            "string": string
        }
        request = CLIENT.post('/assets/metadata/', data=data, format='json')
        self.assertEqual(request.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertIn('detail', request.data)
        self.assertEqual(request.data['detail'], 'Authentication credentials were not provided.')
