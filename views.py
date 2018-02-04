from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template import loader
from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError

from .workers import recipes_as_tables, ingredients_as_tables, i_types_as_tables
from .forms import RecipeForm, IngredientForm, IngredientTypeForm
from .models import Recipe, Ingredient, IngredientType


# Create your views here.
LOGIN_PAGE = '/cookbook/login/'
MAIN_PAGE = '/cookbook/recipes/'

def login_page(request):
    template = loader.get_template('login.html')
    context = {'next': request.GET['next'] if request.GET and 'next' in request.GET else MAIN_PAGE,
               'login_unsuccessful': request.GET and 'login_fail' in request.GET and request.GET['login_fail']=="true",
               'logged_out': request.GET and 'logout' in request.GET and request.GET['logout'] == "true"}
    return HttpResponse(template.render(context, request))

def check_user(request):
    username = request.POST["uname"]
    password = request.POST["pwd"]
    next = request.POST["next"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if next and len(next)>0:
            return redirect(next)
        else:
            return HttpResponse("OK!")
    else:
        return redirect(LOGIN_PAGE + '?next=' + next + "&login_fail=true")

@login_required(login_url=LOGIN_PAGE)
def log_out(request):
    logout(request)
    return redirect(LOGIN_PAGE + '?logout=true')

# Recipes

@login_required(login_url=LOGIN_PAGE)
def recipes(request, alert=None):
    template = loader.get_template('recipes.html')
    context = {'name': request.user.first_name, 'lastname': request.user.last_name, 'recipes': recipes_as_tables(),
                'alert': alert}
    return HttpResponse(template.render(context, request))

@login_required(login_url=LOGIN_PAGE)
def add_recipe(request):
    template = loader.get_template('edit.html')
    alert = None
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            alert = form.create_recipe()
            if alert is None:
                alert = {
                    "class": "success",
                    "header": "Успех!",
                    "text": "Рецепт добавлен в базу"
                }
                form = RecipeForm()
        else:
            alert = {
                "class": "danger",
                "header": "Форма некорректна!",
                "text": "Миша, всё хуйня, давай по новой"
            }
    else:
        form = RecipeForm()
    context = {'name': request.user.first_name, 'lastname': request.user.last_name, 'recipes': recipes_as_tables(),
                'alert': alert, 'form': form, 'element': 'recipes', 'operation': 'add',
                'page_name': "Добавление рецепта",
                'page_description': "Добавление рецепта в базу",
                'page_header_name': "Добавление рецепта",
                'form_address': "forms/recipe.html"}
    return HttpResponse(template.render(context, request))

@login_required(login_url=LOGIN_PAGE)
def edit_recipe(request, operation=None, rcp_in=None):
    template = loader.get_template('edit.html')
    alert = None
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            alert = form.edit_recipe(rcp_in)
            if alert is None:
                alert = {
                    "class": "success",
                    "header": "Успех!",
                    "text": "Рецепт успешно изменён"
                }
                form = RecipeForm()
                return redirect('recipes-all')
        else:
            alert = {
                "class": "danger",
                "header": "Форма некорректна!",
                "text": "Миша, всё хуйня, давай по новой"
            }
    else:
        form = RecipeForm()
        try:
            form.import_recipe(Recipe.objects.get(uid=rcp_in))
        except:
            raise Http404("Рецепт не найден")
    context = {'name': request.user.first_name, 'lastname': request.user.last_name, 'recipes': recipes_as_tables(),
                'alert': alert, 'form': form, 'element': 'recipes', 'operation': 'edit',
                'page_name': "Редактирование рецепта",
                'page_description': "Редактирование рецепта в базе",
                'page_header_name': "Редактирование рецепта",
                'form_address': "forms/recipe.html"}
    return HttpResponse(template.render(context, request))

@login_required(login_url=LOGIN_PAGE)
def delete_recipe(request, rcp_in=None, alert=None):
    if rcp_in is not None:
        try:
            Recipe.objects.get(uid=rcp_in).delete()
            alert = {
                "class": "success",
                "header": "Успех!",
                "text": "Рецепт успешно удалён"
            }
        except:
            alert = {
                "class": "danger",
                "header": "Что-то пошло не так",
                "text": "Не удалось удалить рецепт"
            }

    else:
        alert = {
                "class": "danger",
                "header": "Что-то пошло не так",
                "text": "Не удалось удалить рецепт"
            }
    return redirect('recipes-all')

# Ingredients

@login_required(login_url=LOGIN_PAGE)
def ingredients(request, alert=None):
    template = loader.get_template('ingredients.html')
    context = {'name': request.user.first_name, 'lastname': request.user.last_name, 'ingredients': ingredients_as_tables(),
                'alert': alert}
    return HttpResponse(template.render(context, request))

@login_required(login_url=LOGIN_PAGE)
def add_ingredient(request, alert=None):
    template = loader.get_template('edit.html')
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            if alert is None:
                form.save()
                alert = {
                    "class": "success",
                    "header": "Успех!",
                    "text": "Ингредиент добавлен в базу"
                }
                form = IngredientForm()
        else:
            alert = {
                "class": "danger",
                "header": "Форма некорректна!",
                "text": "Миша, всё хуйня, давай по новой"
            }
    else:
        form = IngredientForm()
    context = {'name': request.user.first_name, 'lastname': request.user.last_name,
                'alert': alert, 'form': form, 'element': 'ingredients', 'operation': 'add',
                'page_name': "Добавление ингредиента",
                'page_description': "Добавление ингредиента в базу",
                'page_header_name': "Добавление ингредиента",
                'form_address': "forms/ingredient.html"}
    return HttpResponse(template.render(context, request))

@login_required(login_url=LOGIN_PAGE)
def edit_ingredient(request, ingr_in):
    template = loader.get_template('edit.html')
    alert = None
    try:
        ingr = Ingredient.objects.get(id=ingr_in)
    except:
        raise Http404("Ингредиент не найден")
    if request.method == "POST":
        form = IngredientForm(request.POST, instance=ingr)
        if form.is_valid():
            form.save()
            alert = {
                "class": "success",
                "header": "Успех!",
                "text": "Ингредиент успешно изменён"
            }
            return redirect('ingredients-all')
        else:
            alert = {
                "class": "danger",
                "header": "Ошибка",
                "text": "Не удалось отредактировать ингредиент"
            }
    else:
        form = IngredientForm(instance=ingr)
    context = {'name': request.user.first_name, 'lastname': request.user.last_name,
                'alert': alert, 'form': form, 'element': 'ingredients', 'operation': 'edit',
                'page_name': "Редактирование ингредиента",
                'page_description': "Редактирование ингредиента в базе",
                'page_header_name': "Редактирование ингредиента",
                'form_address': "forms/ingredient.html"}
    return HttpResponse(template.render(context, request))
    
@login_required(login_url=LOGIN_PAGE)
def delete_ingredient(request, ingr_in):
    try:
        ingr = Ingredient.objects.get(id=ingr_in)
        try:
            ingr.delete()
        except ProtectedError:
            raise PermissionDenied
    except:
        raise Http404("Ингредиент не найден")
    return redirect('ingredients-all')

# Ingredient Types


@login_required(login_url=LOGIN_PAGE)
def i_types(request, alert=None):
    template = loader.get_template('i_types.html')
    context = {'name': request.user.first_name, 'lastname': request.user.last_name, 'i_types': i_types_as_tables(),
                'alert': alert}
    return HttpResponse(template.render(context, request))

@login_required(login_url=LOGIN_PAGE)
def add_i_type(request, alert=None):
    template = loader.get_template('edit.html')
    if request.method == "POST":
        form = IngredientTypeForm(request.POST)
        if form.is_valid():
            if alert is None:
                form.save()
                alert = {
                    "class": "success",
                    "header": "Успех!",
                    "text": "Тип ингредиента добавлен в базу"
                }
                form = IngredientTypeForm()
        else:
            alert = {
                "class": "danger",
                "header": "Форма некорректна!",
                "text": "Миша, всё хуйня, давай по новой"
            }
    else:
        form = IngredientTypeForm()
    context = {'name': request.user.first_name, 'lastname': request.user.last_name,
                'alert': alert, 'form': form, 'element': 'i_types', 'operation': 'add',
                'page_name': "Добавление типа ингредиента",
                'page_description': "Добавление типа ингредиента в базу",
                'page_header_name': "Добавление типа ингредиента",
                'form_address': "forms/i_type.html"}
    return HttpResponse(template.render(context, request))

@login_required(login_url=LOGIN_PAGE)
def edit_i_type(request, ingr_in):
    template = loader.get_template('edit.html')
    alert = None
    try:
        ingr = IngredientType.objects.get(id=ingr_in)
    except:
        raise Http404("Тип ингредиента не найден")
    if request.method == "POST":
        form = IngredientTypeForm(request.POST, instance=ingr)
        if form.is_valid():
            form.save()
            alert = {
                "class": "success",
                "header": "Успех!",
                "text": "Тип ингредиента успешно изменён"
            }
            return redirect('i_types-all')
        else:
            alert = {
                "class": "danger",
                "header": "Ошибка",
                "text": "Не удалось отредактировать тип ингредиента"
            }
    else:
        form = IngredientTypeForm(instance=ingr)
    context = {'name': request.user.first_name, 'lastname': request.user.last_name,
                'alert': alert, 'form': form, 'element': 'i_types', 'operation': 'edit',
                'page_name': "Редактирование типа ингредиента",
                'page_description': "Редактирование типа ингредиента в базе",
                'page_header_name': "Редактирование типа ингредиента",
                'form_address': "forms/i_type.html"}
    return HttpResponse(template.render(context, request))
    
@login_required(login_url=LOGIN_PAGE)
def delete_i_type(request, ingr_in):
    try:
        ingr = IngredientType.objects.get(id=ingr_in)
        try:
            ingr.delete()
        except ProtectedError:
            raise PermissionDenied
    except:
        raise Http404("Тип ингредиента не найден")
    return redirect('i_types-all')
