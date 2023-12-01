from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            return ValueError('Email is required!')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.create_activation_code()
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_customer', True)
        return self._create_user(email, password, **kwargs)

    def create_courier(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_customer', True)
        kwargs.setdefault('is_courier', True)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_customer', True)
        kwargs.setdefault('is_courier', True)
        return self._create_user(email, password, **kwargs)

    def create_employee(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_customer', True)
        kwargs.setdefault('is_courier', True)
        return self._create_user(email, password, **kwargs)


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=220)
    phone_number = models.CharField(max_length=25, blank=True, null=True, unique=True)
    activation_code = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False)

    username = None
    groups = None
    user_permissions = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code


