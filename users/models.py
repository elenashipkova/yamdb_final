from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField('email адрес', unique=True)
    username = models.CharField(
        'Псевдоним',
        max_length=150,
        unique=True,
        help_text=('Обязательное поле, только цифры, буквы или @/./+/-/_.'
                   ),
        validators=[username_validator],
        error_messages={
            'unique': ('Пользователь с этим именем уже существует.'),
        },
    )
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    bio = models.CharField('Информация о пользователе',
                           max_length=300, blank=True, null=True)
    role = models.CharField('Права доступа',
                            max_length=16,
                            choices=CHOICES,
                            default=CHOICES[0])
    password = models.CharField('Пароль', max_length=128)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class RegistrationEmail(models.Model):
    email = models.EmailField('email адрес', unique=True)
    confirmation_code = models.CharField('Код подтверждения', max_length=10)

    class Meta:
        verbose_name = 'Email для аутентификации'
        verbose_name_plural = 'Email для аутентификации'
