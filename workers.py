from .models import Recipe, Ingredient, IngredientType

def recipe_as_table(rcp):
    out_recipe = {}
    out_recipe["name"] = rcp.name
    out_recipe["category"] = rcp.get_category_display()
    ingrs = []
    for i in rcp.ingredientamount_set.all():
        amnt = i.amount if not i.amount.is_integer() else int(i.amount)
        ingrs.append("{} - {} {}".format(i.ingredient.name, amnt, i.units))
    out_recipe["ingredients"] = ingrs
    if rcp.description is not None and len(rcp.description) > 0:
        out_recipe["description"] = rcp.description
    if rcp.url is not None and len(rcp.url) > 0:
        out_recipe["url"] = rcp.url
    tags = []
    for t in rcp.tags.all():
        tags.append(t.name)
    out_recipe["tags"] = tags
    out_recipe["uid"] = rcp.uid
    return out_recipe

def recipes_as_tables():
    out_recipes = []
    for r in Recipe.objects.all():
        out_recipes.append(recipe_as_table(r))
    return out_recipes

def ingredient_as_table(ingr):
    out_ingr = {}
    out_ingr["id"] = ingr.id
    out_ingr["name"] = ingr.name
    out_ingr["type_name"] = ingr.i_type.name
    out_ingr["recipes"] = []
    for iam in ingr.ingredientamount_set.all():
        rcp = {"name": iam.recipe.name, "type": iam.recipe.get_category_display()}
        if rcp not in out_ingr["recipes"]:
            out_ingr["recipes"].append(rcp)
    return out_ingr

def ingredients_as_tables():
    out_ingrs = []
    for i in Ingredient.objects.all():
        out_ingrs.append(ingredient_as_table(i))
    return out_ingrs

def i_type_as_table(i_type):
    out_i_type = {}
    out_i_type["id"] = i_type.id
    out_i_type["name"] = i_type.name
    out_i_type["ingredients"] = []
    for ingr in i_type.ingredient_set.all():
        if ingr.name not in out_i_type["ingredients"]:
            out_i_type["ingredients"].append(ingr.name)
    out_i_type["recipes"] = []
    for rcp in Recipe.objects.filter(ingredients__i_type__name=i_type.name):
        r = {"name": rcp.name, "type": rcp.get_category_display()}
        if r not in out_i_type["recipes"]:
            out_i_type["recipes"].append(r)
    return out_i_type

def i_types_as_tables():
    out_i_types = []
    for i in IngredientType.objects.all():
        out_i_types.append(i_type_as_table(i))
    return out_i_types
    
