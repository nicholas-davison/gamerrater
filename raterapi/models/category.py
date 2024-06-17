from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    games = models.ManyToManyField(
        "Game",
        through="GameCategory",
        related_name="categories"
    )