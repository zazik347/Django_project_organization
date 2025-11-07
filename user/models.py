from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_ip = models.GenericIPAddressField(blank=True, null=True)  # IP при регистрации
    login_ip = models.GenericIPAddressField(blank=True, null=True)  # IP при входе
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Профиль {self.user.username}'


