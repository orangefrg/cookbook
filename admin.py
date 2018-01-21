from django.contrib import admin

from .models import IngredientType, Ingredient, RecipeTag, Nutrient, Nutrition
from .models import NutrientAmount, Recipe, IngredientAmount

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'i_type')

# Register your models here.
admin.site.register(IngredientType)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount)
admin.site.register(Recipe)
admin.site.register(RecipeTag)
admin.site.register(Nutrition)
admin.site.register(Nutrient)
admin.site.register(NutrientAmount)