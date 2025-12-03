from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Article, Podcast, PressRelease


class HomeSitemap(Sitemap):
    changefreq = "always"
    priority = 1.0

    def items(self):
        return ["home"]  # name of your URL pattern for homepage

    def location(self, item):
        return reverse(item)

# 📄 Static Pages
class StaticViewSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.3

    def items(self):
        return ["about" , "privacy_policy" , "terms_of_service" , "cookie_policy" , "contact"]  # add more URL names if needed (about, contact, etc.)

    def location(self, item):
        return reverse(item)


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, "updated_at") else obj.created_at

class PodcastSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Podcast.objects.all()

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, "updated_at") else obj.published_at


class PressReleaseSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return PressRelease.objects.all()

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, "updated_at") else obj.created_at
