from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """test the users API public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """test creating user with valid payload is successful"""
        payload = {
            'email': 'batman@me.com',
            'password': 'test__',
            'name': 'bruce'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """test creating a user already exists fails"""
        payload = {
            'email': 'spiderman@me.com',
            'password': 'test!?',
            'name': 'Pieter'
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test that password must be more than 5 characters"""
        payload = {
            'email': 'joker@me.com',
            'password': 'ts',
            'name': 'Joker'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """test that token is created for the user"""
        payload = {
            'email': 'joker@me.com',
            'password': 'hahaha'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        """test that token will not be created"""
        payload = {
            'email': 'joker@me.com',
            'password': 'hahaha'
        }
        create_user(**payload)
        payload['password'] = 'batman'
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_no_user(self):
        """test that token will not be created"""
        payload = {'email': 'joker@me.com', 'password': 'hahaha'}
        payload['password'] = 'batman'
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_with_missing_field(self):
        """test that token will not be created"""
        payload = {
            'email': 'joker@me.com',
            'password': 'hahaha'
        }
        create_user(**payload)
        del payload['email']
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
