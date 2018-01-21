import uuid
from django.db import models

RECIPE_CATEGORY = (
    ("SNACK", "Закуска"),
    ("MAIN", "Основное блюдо"),
    ("SIDE", "Гарнир"),
    ("DESSERT", "Десерт"),
    ("BREAKFAST", "Завтрак"),
    ("DRINK", "Напиток"),
    ("SOUP", "Суп"),
    ("SAUCE", "Соус"),
    ("OTHER", "Прочее"))

class IngredientType(models.Model):
    name = models.CharField(unique=True)

class Ingredient(models.Model):
    i_type = models.ForeignKey(IngredientType, on_delete=models.PROTECT)
    name = models.CharField(unique=True)

class RecipeTag(models.Model):
    name = models.CharField()

class Nutrient(models.Model):
    name = models.FloatField()
    is_allergic = models.BooleanField(default=False)
    is_healthy = models.BooleanField(default=False)

class Nutrition(models.Model):
    protein = models.FloatField()
    fat = models.FloatField()
    carbohydrate = models.FloatField()
    energy = models.FloatField()
    nutrients = models.ManyToManyField(
        Nutrient,
        through='NutrientAmount',
        through_fields=('nutrition', 'nutrient'),
        null=True,
        blank=True
    )

class Recipe(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True)
    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        through_fields=('recipe', 'ingredient'),
    )
    tags = models.ManyToManyField(RecipeTag, null=True, blank=True)
    category = models.CharField(max_length=15, choices=RECIPE_CATEGORY)
    nutrition = models.ForeignKey(Nutrition, null=True, blank=True)

class IngredientAmount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    amount = models.FloatField()
    units = models.CharField(null=True, blank=True)