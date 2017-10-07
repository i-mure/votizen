from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.user_login, name='login'),
    url(r'^accounts/login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^accounts/logout/', views.user_logout, name='logout'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^voting/', views.voting, name='voting'),
    url(r'^vote/(?P<recipient>.*)/$', views.vote, name='vote'),

    url(r'^results/', views.leader_board, name='leader_board'),
    url(r'^results_api/', views.results_api, name='results_api'),


    url(r'^$', views.home, name='home'),
]
