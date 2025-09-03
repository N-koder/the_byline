from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:category_name>/', views.category_articles, name='category_articles'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('tag/<slug:slug>/', views.tagged_articles, name="tagged_articles"),
    path('author/<str:username>/', views.author_articles, name="author_articles"),
    path('contact/', views.contact, name='contact'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('cookie-policy/', views.cookie_policy, name='cookie_policy'),
    path('blog/autosave/', views.autosave_draft, name='autosave_draft'),
    
    path("ads.txt", TemplateView.as_view(
        template_name="blog/ads.txt",
        content_type="text/plain"
    )),
]
