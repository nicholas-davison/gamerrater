from django.db import models
from django.contrib.auth.models import User

class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_images')
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='game_images')
    image = models.ImageField(upload_to='game_images/')