from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    username = models.CharField(
        verbose_name='username', max_length=150, unique=True)
    email = models.EmailField(
        verbose_name='email address', max_length=254, unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(max_length=10, choices=CHOICES, default='user')

    confirmation_code = models.CharField(max_length=256, blank=True)
    
    key_expires = models.DateTimeField()

    @property
    def is_admin(self):
        "User ia admin?"
        return self.role == 'admin'

    @property
    def is_moderator(self):
        "User moderator?"
        return self.role == 'moderator'
