from django.contrib.auth.models import User, AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.conf import settings


class CustomUser(AbstractUser):
    """
    Пользовательская модель User с авторизацией по полям email и password
    """
    username = None
    email = models.EmailField("email адрес", unique=True)
    role = models.PositiveSmallIntegerField(verbose_name='Роль',
                                            choices=settings.USER_ROLE_CHOICES, default=settings.UNDEFINED)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

