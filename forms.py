from django import forms
from .models import *
import re

class RecipeForm(forms.Form):
    recipe_name = forms.CharField(label = "Название", required = True, strip = True, max_length = 200)
    category = forms.ChoiceField(label = "Категория", choices = RECIPE_CATEGORY, required = True)
    url = forms.URLField(label = "Адрес", required = False)
    description = forms.CharField(label = "Описание", required = False, strip = True, widget = forms.Textarea)
    tags = forms.ModelMultipleChoiceField(label = "Тэги", queryset = RecipeTag.objects.all(), required = False)
    
    ingredient_count = forms.IntegerField(widget=forms.HiddenInput(), label="Ингредиенты")

    def __init__(self, *args, **kwargs):
        ingredient_count = 1
        if len(args) > 0 and args[0]["ingredient_count"] is not None and int(args[0]["ingredient_count"]) > 1:
            ingredient_count = args[0]["ingredient_count"]
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields["ingredient_count"].initial = ingredient_count

        for i in range(int(ingredient_count)):
            self.fields["ingredient_{}".format(i)] = forms.ModelChoiceField(
                label = "Ингредиент",
                help_text = "Выберите ингредиент",
                queryset = Ingredient.objects.all()
            )
            self.fields["amount_{}".format(i)] = forms.CharField(
                label = "Количество",
                help_text = "Укажите количество"
            )

    def import_recipe(self, recipe):
        self.fields["recipe_name"].initial = recipe.name
        self.fields["category"].initial = recipe.category
        self.fields["url"].initial = recipe.url
        self.fields["description"].initial = recipe.description
        self.fields["tags"].initial = recipe.tags.all()
        ingrs = recipe.ingredients.all()
        self.fields["ingredient_count"].initial = ingrs.count()
        i = 0
        for ingr in recipe.ingredientamount_set.all():
            self.fields["ingredient_{}".format(i)] = forms.ModelChoiceField(
                label = "Ингредиент",
                help_text = "Выберите ингредиент",
                queryset = Ingredient.objects.all(),
                initial = ingr.ingredient
            )
            self.fields["amount_{}".format(i)] = forms.CharField(
                label = "Количество",
                help_text = "Укажите количество",
                initial = "{} {}".format(ingr.amount, ingr.units)
            )
            i += 1

    def create_recipe(self):
        cdata = self.cleaned_data
        description = cdata["description"]
        url = cdata["url"]
        if (description is None or len(description) == 0) and (url is None or len(url) == 0):
            return {"header": "Неверное описание рецепта",
                    "class": "danger",
                    "text": "У рецепта должно быть описание или адрес"}
        rcp = Recipe(
            name = cdata["recipe_name"],
            description = description,
            url = url,
            category = cdata["category"]
        )
        out_errors = []
        out_ingr = []
        for i in range(cdata["ingredient_count"]):
            amount_form = cdata["amount_{}".format(i)]
            ingredient_form = cdata["ingredient_{}".format(i)]
            rg = re.compile("(([\.]*)(\d+)([\.,]*)(\d*))(\s*)(((\s*)([а-яА-Яa-zA-Z0-9]+))*)$")
            amount_match = rg.match(amount_form)
            success = True
            amount = None
            units = None
            if not amount_match:
                out_errors.append("не удалось найти количество в строке \"{}\"".format(amount_form))
            else:
                try:
                    amount = float(amount_match.group(1))
                    units = amount_match.group(7)
                except:
                    out_errors.append("не удалось распознать количество в строке \"{}\"".format(amount_form))
                    success = False
            if success:
                ingr = IngredientAmount(
                    recipe = rcp,
                    ingredient = ingredient_form,
                    amount = amount,
                    units = units
                )
                out_ingr.append(ingr)
        if len(out_errors) == 0:
            rcp.save()
            for ing in out_ingr:
                ing.save()         
            rcp.tags.set(cdata["tags"])
            return None
        else:
            return {"header": "Ошибки в форме",
                    "class": "danger",
                    "text": "Возникли следующие проблемы: {}".format(", ".join(out_errors))}

    def edit_recipe(self, recipe_uid):
        cdata = self.cleaned_data
        description = cdata["description"]
        url = cdata["url"]
        if (description is None or len(description) == 0) and (url is None or len(url) == 0):
            return {"header": "Неверное описание рецепта",
                    "class": "danger",
                    "text": "У рецепта должно быть описание или адрес"}
        recipe = Recipe.objects.get(uid=recipe_uid)
        recipe.name = cdata["recipe_name"]
        recipe.description = description
        recipe.url = url
        recipe.category = cdata["category"]


        out_errors = []
        out_ingr = []
        for i in range(cdata["ingredient_count"]):
            amount_form = cdata["amount_{}".format(i)]
            ingredient_form = cdata["ingredient_{}".format(i)]
            rg = re.compile("(([\.]*)(\d+)([\.,]*)(\d*))(\s*)(((\s*)([а-яА-Яa-zA-Z0-9]+))*)$")
            amount_match = rg.match(amount_form)
            success = True
            amount = None
            units = None
            if not amount_match:
                out_errors.append("не удалось найти количество в строке \"{}\"".format(amount_form))
            else:
                try:
                    amount = float(amount_match.group(1))
                    units = amount_match.group(7)
                except:
                    out_errors.append("не удалось распознать количество в строке \"{}\"".format(amount_form))
                    success = False
            if success:
                ingr = IngredientAmount(
                    recipe = recipe,
                    ingredient = ingredient_form,
                    amount = amount,
                    units = units
                )
                out_ingr.append(ingr)

        if len(out_errors) == 0:
            recipe.ingredientamount_set.all().delete()
            for ing in out_ingr:
                ing.save()     
            recipe.save()
            recipe.tags.set(cdata["tags"])    
            return None

                
