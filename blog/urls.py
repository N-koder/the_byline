from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
     path('category/<str:category_name>/', views.category_articles, name='category_articles'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
]
