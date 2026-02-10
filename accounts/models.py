from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [
    ('Teacher', 'O\'qituvchi'),
    ('Student', 'Talaba'),
]


class User(AbstractUser):
    """Custom user: role va added_at."""
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Student')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return self.username

    @property
    def is_teacher(self):
        return self.role == 'Teacher'

    @property
    def is_student(self):
        return self.role == 'Student'
