from django.db import models

# Create your models here.
class Ingredients(models.Models):
    name = models.CharField(max_length=120)
    def __str__(self):
        return self.name