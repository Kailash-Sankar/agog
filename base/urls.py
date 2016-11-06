from django.conf.urls import url
from . import views

urlpatterns = [
    #Home
    url(r'^$', views.home, name='home'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),

    #Auth
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    
    #meta debug       
    url(r'^meta/$', views.display_meta, name='meta'),
     
    #Views
    url(r'^ask/$', views.ask, name='ask'),    
    url(r'^question/([0-9]+)$', views.view_question, name='view_question'),
    
    #Q&A
    url(r'^q/([0-9]+)$', views.question, name='question'),
    url(r'^question/([0-9]+)/answers/([0-9]*)$', views.answers, name='answers'),
    url(r'^tags/([a-zA-Z]+)$', views.tags, name='tags'),

    #Tending
    url(r'^trending/([a-zA-Z]+)$', views.trending, name='trending'),

    #like
    url(r'^question/([0-9]+)/like$', views.qlike, name='qlike'),
    url(r'^answer/([0-9]+)/like$', views.alike, name='alike'),

    #save
    url(r'^question/save$', views.saveQuestion, name='saveq'),   
    url(r'^question/([0-9]+)/answer/save$', views.saveAnswer, name='savea'),   

    #profile
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^me/$', views.me, name='me'),
    url(r'^me/tags$', views.userTags, name='userTags'),
    url(r'^me/tags/save$', views.saveUserTags, name='saveUserTags'),
] 