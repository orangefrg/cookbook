from .models import Recipe

def recipe_as_table(rcp):
    out_recipe = {}
    out_recipe["name"] = rcp.name
    out_recipe["category"] = rcp.get_category_display()
    ingrs = []
    for i in rcp.ingredientamount_set.all():
        amnt = i.amount if not i.amount.is_integer() else int(i.amount)
        ingrs.append("{} - {} {}".format(i.ingredient.name, amnt, i.units))
    out_recipe["ingredients"] = ingrs
    out_recipe["description"] = rcp.description
    out_recipe["url"] = rcp.url
    tags = []
    for t in rcp.tags.all():
        tags.append(t.name)
    out_recipe["tags"] = tags
    return out_recipe

def recipes_as_tables():
    out_recipes = []
    for r in Recipe.objects.all():
        out_recipes.append(recipe_as_table(r))
    return out_recipes