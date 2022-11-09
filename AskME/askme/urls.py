#askme URL Configuration

from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('ask', views.ask, name='ask'),
    path('settings', views.settings, name='settings'),
    path('question', views.question, name='question'),
    #path('question/<int:id>', views.question, name='question'),
    path('tag', views.tag, name='tag'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
]
