from django.contrib.auth.models import User, AbstractUser
from django.db import models
from .managers import CustomUserManager, TeacherManager, StudentManager, UndefinedUserManager
from django.conf import settings


class CustomUser(AbstractUser):
    """
    Пользовательская модель User с авторизацией по полям email и password
    """
    username = None
    email = models.EmailField("email адрес", unique=True)
    role = models.PositiveSmallIntegerField(verbose_name='Роль',
                                            choices=settings.USER_ROLE_CHOICES, default=settings.STUDENT)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    teachers = TeacherManager()
    students = StudentManager()
    undefined_users = UndefinedUserManager()

    def __str__(self):
        return self.email

