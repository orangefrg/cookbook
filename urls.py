from django.conf.urls import url, include
from django.contrib import admin
from cookbook.views import recipes, login_page, log_out, check_user

admin.autodiscover()

urlpatterns = [
               url(r'^recipes/$', recipes, name='recipes-all'),
               url(r'^login/$', login_page, name='login'),
               url(r'^logout/$', log_out, name='logout'),
               url(r'^check_user/$', check_user, name='check_user'),
               ]
