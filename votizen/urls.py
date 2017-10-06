from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^signup/', views.signup, name='signup'),

    url(r'^voting/', views.voting, name='voting'),
    url(r'^$', views.home, name='home'),
]
