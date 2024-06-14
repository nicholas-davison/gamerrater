from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_created')
    title = models.CharField(max_length=255)
    description = models.TextField()
    designer = models.CharField(max_length=255)
    year_released = models.PositiveIntegerField()
    number_of_players = models.PositiveIntegerField()
    estimated_play_time = models.PositiveIntegerField()
    age_recommendation = models.PositiveIntegerField()
    categories = models.ManyToManyField(
        "Category",
        through='GameCategory',
        related_name="games"
    )