from django.contrib import admin
from django.urls import path
from django.conf.urls import handler400, handler500
from . import views
app_name = "article"

urlpatterns = [
    path('dashboard/',views.dashboard,name = "dashboard"),
    path('addarticle/',views.addArticle,name = "addarticle"),
    path('article/<str:title>/',views.detail,name = "detail"),
    path('update/<str:title>',views.updateArticle,name = "update"),
    path('delete/<str:title>',views.deleteArticle,name = "delete"),
    path('',views.articles,name = "articles"),
    # path('comment/<str:title>',views.addComment,name = "comment"),
    
]
