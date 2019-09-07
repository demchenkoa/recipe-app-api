from django.test import TestCase
from django.contrib.auth import get_user_model


class ModerTests(TestCase):

    def test_create_user_with_email_successful(self):
        """test creating a new user with email is OK"""
        email = 'alex@i.com'
        password = 'summer19'
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test email for a new user is normalized"""
        email = 'alex@INFO.com'
        user = get_user_model().objects.create_user(email, 'alex')

        self.assertEqual(user.email, email.lower())
