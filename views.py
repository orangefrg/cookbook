from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template import loader


# Create your views here.
LOGIN_PAGE = '/cookbook/login/'
MAIN_PAGE = '/ewhouse/recipes/'

def login_page(request):
    template = loader.get_template('login.html')
    context = {'next': request.GET['next'] if request.GET and 'next' in request.GET else MAIN_PAGE,
               'login_unsuccessful': request.GET and 'login_fail' in request.GET and request.GET['login_fail']=="true",
               'logged_out': request.GET and 'logout' in request.GET and request.GET['logout'] == "true"}
    return HttpResponse(template.render(context, request))

@login_required(login_url=LOGIN_PAGE)
def recipes(request):
    template = loader.get_template('recipes.html')
    context = {'name': request.user.first_name, 'lastname': request.user.last_name}
    return HttpResponse(template.render(context, request))