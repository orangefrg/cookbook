from django.urls import path, re_path
from django.contrib import admin
from cookbook.views import recipes, login_page, log_out, check_user, add_recipe, edit_recipe, delete_recipe

admin.autodiscover()

urlpatterns = [
               path(r'recipes/', recipes, name='recipes-all'),
               path(r'recipes/edit', add_recipe, name='recipes-add'),
               path(r'recipes/edit/<slug:rcp_in>', edit_recipe, name='recipes-edit'),
               path(r'recipes/delete/<slug:rcp_in>', delete_recipe, name='recipes-delete'),
               path(r'login/', login_page, name='login'),
               path(r'logout/', log_out, name='logout'),
               path(r'check_user/', check_user, name='check_user'),
               ]
