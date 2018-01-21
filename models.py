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
    name = models.CharField(unique=True, max_length=200, verbose_name="Наименование")
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Тип ингредиента"
        verbose_name_plural = "Типы ингредиентов"


class Ingredient(models.Model):
    i_type = models.ForeignKey(IngredientType, on_delete=models.PROTECT, verbose_name="Тип")
    name = models.CharField(unique=True, max_length=200, verbose_name="Наименование")
    def __str__(self):
        return "{} ({})".format(self.name, self.i_type.name)

    class Meta:
        ordering = ['name']
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class RecipeTag(models.Model):
    name = models.CharField(unique=True, max_length=200)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Тег рецепта"
        verbose_name_plural = "Теги рецептов"

class Nutrient(models.Model):
    name = models.CharField(unique=True, max_length=200, verbose_name="Наименование")
    is_allergic = models.BooleanField(default=False)
    is_healthy = models.BooleanField(default=False)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Пищевой компонент"
        verbose_name_plural = "Пищевые компоненты"

class Nutrition(models.Model):
    protein = models.FloatField()
    fat = models.FloatField()
    carbohydrate = models.FloatField()
    energy = models.FloatField()
    nutrients = models.ManyToManyField(
        Nutrient,
        through='NutrientAmount',
        through_fields=('nutrition', 'nutrient'),
        blank=True
    )


class NutrientAmount(models.Model):
    nutrition = models.ForeignKey(Nutrition, on_delete=models.PROTECT)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.PROTECT)
    amount = models.FloatField()


class Recipe(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=200, verbose_name="Название")
    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        through_fields=('recipe', 'ingredient')
    )
    tags = models.ManyToManyField(RecipeTag, blank=True)
    category = models.CharField(max_length=15, choices=RECIPE_CATEGORY)
    nutrition = models.ForeignKey(Nutrition, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def get_all_ingredients(self):
        ret = {}
        for i in self.ingredients.all():
            if i.ingredient.name in ret:
                if i.units in ret[i.ingredient.name]:
                    ret[i.ingredient.name][i.units] += i.amount
                else:
                    ret[i.ingredient.name][i.units] = i.amount
            else:
                ret[i.ingredient.name] = i.units
                ret[i.ingredient.name][i.units] = i.amount
        return ret

    class Meta:
        ordering = ['name']
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

class IngredientAmount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    amount = models.FloatField()
    units = models.CharField(max_length=50, null=True, blank=True)