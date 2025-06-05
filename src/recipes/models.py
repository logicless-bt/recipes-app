from django.db import models

# Create your models here.
class Recipe(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=120)
    cooking_time = models.IntegerField()
    ingredients = models.TextField(default="")
    separate_ingredients = models.TextField(default="", blank=True, null=True)
    difficulty = models.TextField(default="")
    description = models.TextField(default="")
    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')

    def __str__(self):
        return str(self.name)
    
    def calculate_difficulty(self):
        ing_num = len(self.separate_ingredients)
        if ing_num < 4 and self.cooking_time < 10:
            self.difficulty = "Easy"
        if ing_num < 4 and self.cooking_time >= 10:
            self.difficulty = "Medium"
        if ing_num >= 4 and self.cooking_time < 10:
            self.difficulty = "Intermediate"
        if ing_num >= 4 and self.cooking_time >= 10:
            self.difficulty = "Hard"

    def separate_ingredients_by_comma(self):
        self.separate_ingredients = self.ingredients.split(", ")

    def save(self, *args, **kwargs):
        self.calculate_difficulty()
        super().save(*args, **kwargs)