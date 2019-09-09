from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        """creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """creates a superuser"""
        # passing this params to constructor
        # will prevent unnecessary 2nd call to db
        user = self.create_user(email=email, password=password,
                                is_staff=True, is_superuser=True)

        # example with 2nd call
        # user = self.create_user(email=email, password=password)
        # user.is_staff = True
        # user.is_superuser = True
        # user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model with email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # todo: read that this does
    objects = UserManager()

    # https://docs.djangoproject.com/en/2.2/topics/auth/customizing/
    # this field has to be unique
    USERNAME_FIELD = 'email'
