from django.contrib.sitemaps import Sitemap
from blog.models import Article

class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.updated_at