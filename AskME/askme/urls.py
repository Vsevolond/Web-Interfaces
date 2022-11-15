#askme URL Configuration

from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('ask', views.ask, name='ask'),
    path('settings', views.settings, name='settings'),
    path('question/<int:id>', views.question, name='question'),
    path('tag/<str:question_tag>', views.tag, name='tag'),
    path('hot', views.hot, name='hot'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
