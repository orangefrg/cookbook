from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template import loader
from .workers import recipes_as_tables
from .forms import RecipeForm
from .models import Recipe


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
                'alert': alert, 'form': form, 'element': 'recipes', 'operation': 'add'}
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
        form.import_recipe(Recipe.objects.get(uid=rcp_in))
    context = {'name': request.user.first_name, 'lastname': request.user.last_name, 'recipes': recipes_as_tables(),
                'alert': alert, 'form': form, 'element': 'recipes', 'operation': 'edit'}
    return HttpResponse(template.render(context, request))

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