from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50)  # 'register' или 'login'
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action_type} ({self.timestamp})"
