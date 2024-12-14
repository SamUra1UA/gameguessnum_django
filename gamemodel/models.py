from django.db import models
from django.contrib.auth.models import User

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_number = models.IntegerField()
    target_range = models.IntegerField(default=100)  # Діапазон (0-100 або інший)
    attempts_left = models.IntegerField()
    is_active = models.BooleanField(default=True)
    result = models.CharField(max_length=10, blank=True, null=True)  # Win/Lose
    history = models.JSONField(default=list)  # Для зберігання історії спроб
    created_at = models.DateTimeField(auto_now_add=True)  # Дата створення гри
