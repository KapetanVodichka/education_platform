from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    STUDENT = 'student', 'Студент'
    TEACHER = 'teacher', 'Преподаватель'


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Почта', blank=True, null=True)

    role = models.CharField(max_length=7, choices=UserRole.choices, default=UserRole.STUDENT)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'