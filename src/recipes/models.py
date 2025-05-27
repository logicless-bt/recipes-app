from django.db import models

# Create your models here.
class Recipe(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=120)
    cooking_time = models.IntegerField()
    ingredients = models.TextField(default="")
    difficulty = models.TextField(default="")
    description = models.TextField(default="")

    def __str__(self):
        return str(self.name)
    
