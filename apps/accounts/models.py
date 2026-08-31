from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """Custom user model — logs in with email, not username."""

    ROLE_ADMIN = 'admin'
    ROLE_MEMBER = 'member'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MEMBER, 'Member'),
    ]

    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    avatar = models.ImageField(upload_to='accounts/avatars/', blank=True, null=True)
    is_active_member = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser or self.role == self.ROLE_ADMIN
