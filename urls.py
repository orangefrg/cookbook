from django.conf.urls import url, include
from django.contrib import admin
from cookbook.views import recipes, login_page

admin.autodiscover()

urlpatterns = [
               url(r'^recipes/$', recipes, name='recipes-all'),
               url(r'^login/$', login_page, name='login'),
               ]
