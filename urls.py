from django.urls import path, re_path
from django.contrib import admin
from cookbook.views import login_page, log_out, check_user
from cookbook.views import recipes, add_recipe, edit_recipe, delete_recipe
from cookbook.views import ingredients, add_ingredient, edit_ingredient, delete_ingredient
from cookbook.views import i_types, add_i_type, edit_i_type, delete_i_type

admin.autodiscover()

urlpatterns = [
               path(r'recipes/', recipes, name='recipes-all'),
               path(r'recipes/edit', add_recipe, name='recipes-add'),
               path(r'recipes/edit/<slug:rcp_in>', edit_recipe, name='recipes-edit'),
               path(r'recipes/delete/<slug:rcp_in>', delete_recipe, name='recipes-delete'),
               path(r'ingredients/', ingredients, name='ingredients-all'),
               path(r'ingredients/edit', add_ingredient, name='ingredients-add'),
               path(r'ingredients/edit/<int:ingr_in>', edit_ingredient, name='ingredients-edit'),
               path(r'ingredients/delete/<int:ingr_in>', delete_ingredient, name='ingredients-delete'),
               path(r'i_types/', i_types, name='i_types-all'),
               path(r'i_types/edit', add_i_type, name='i_types-add'),
               path(r'i_types/edit/<int:ingr_in>', edit_i_type, name='i_types-edit'),
               path(r'i_types/delete/<int:ingr_in>', delete_i_type, name='i_types-delete'),
               path(r'login/', login_page, name='login'),
               path(r'logout/', log_out, name='logout'),
               path(r'check_user/', check_user, name='check_user'),
               ]
