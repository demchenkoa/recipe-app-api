from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='alex@me.com', password='alex_test'):
    """create a sample user"""
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):

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

    def test_new_user_invalid_email(self):
        """test user with no email will raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'mypass')

    def test_create_super_user(self):
        """test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            email='test@me.com'
            'mypass'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """test tag representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)
