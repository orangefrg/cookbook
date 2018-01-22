from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template import loader


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
def recipes(request):
    template = loader.get_template('recipes.html')
    context = {'name': request.user.first_name, 'lastname': request.user.last_name}
    return HttpResponse(template.render(context, request))