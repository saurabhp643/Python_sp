from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Prevents conflicts
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Prevents conflicts
        blank=True
    )

    def __str__(self):
        return self.username
