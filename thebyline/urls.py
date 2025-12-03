"""
URL configuration for thebyline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView, RedirectView
from django.templatetags.static import static
from .sitemaps import HomeSitemap, StaticViewSitemap, ArticleSitemap, PodcastSitemap, PressReleaseSitemap

sitemaps = {
    "home": HomeSitemap,
    "static": StaticViewSitemap,
    "articles": ArticleSitemap,
    "podcasts": PodcastSitemap,
    "press_releases": PressReleaseSitemap,
}

urlpatterns = [
    path('sec123@/admin/', admin.site.urls),
    path('', include('blog.urls')),  # ← include your blog URLs here
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    # Ensure Google and browsers can fetch favicon at the root
    path('favicon.ico', RedirectView.as_view(url=static('blog/images/Logo.ico'), permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
