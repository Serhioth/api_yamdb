from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Переопределённая модель пользователя"""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.is_superuser:
            self.role = 'admin'

    email = models.EmailField(
        'Почта',
        unique=True,
        max_length=254,
        help_text='Почта пользователя'
    )

    bio = models.TextField(
        'Описание',
        blank=True,
        null=True,
        help_text='Описание пользователя'
    )

    role = models.CharField(
        'Статус',
        choices=ROLES,
        max_length=9,
        default='user',
        help_text='Статус пользователя'
    )

    REQUIRED_FIELDS = ('email', )

    def __str__(self) -> str:
        """Переопределённый метод __str__"""
        return self.username

    @property
    def is_admin(self):
        """Метод проверки статуса администратора"""
        return self.is_superuser or self.role == self.ADMIN

    @property
    def is_moderator(self):
        """Метод проверки статуса модератора"""
        return self.role == self.MODERATOR
