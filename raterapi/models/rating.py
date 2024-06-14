from django.db import models
from django.contrib.auth.models import User

class Rating(models.Model):
    RATING_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    ]
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)