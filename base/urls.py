from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),

    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
       
    url(r'^meta/$', views.display_meta, name='meta'),
     
    #Question  
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^tags/([a-zA-Z]+)$', views.tags, name='tags'),
    url(r'^question/([0-9]+)$', views.question, name='question'),
    url(r'^question/([0-9]+)/answers/([0-9]*)$', views.answers, name='answers'),
    
    #Tending
    url(r'^trending/([a-zA-Z]+)$', views.trending, name='trending'),

    #like
    #url(r'^question/([0-9]+)/like$', views.like, name='like'),
    url(r'^answer/([0-9]+)/like$', views.like, name='like'),
] 