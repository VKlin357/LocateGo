from django.db import models
from users.models import User

class Application(models.Model):
    ACTIVITY_CHOICES = [
        ('travel', 'Travel'),
        ('sport', 'Sport'),
        ('music', 'Music'),
        # Добавьте другие активности
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    activity = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    experience_level = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
