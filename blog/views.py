from django.shortcuts import render, get_object_or_404
from .models import Article

# views.py
from django.shortcuts import render
from .models import Article

def home(request, category_slug=None):
    articles = Article.objects.all().order_by('-created_at')
    featured_articles = Article.objects.filter(is_featured=True).order_by('-created_at')[:5]

    context = {
        'articles': articles,
        'featured_articles': featured_articles,
        'current_category': category_slug.capitalize() if category_slug else None
    }
    return render(request, 'blog/home.html', context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'blog/article_detail.html', {'article': article})


def category_articles(request, category_name):
    articles = Article.objects.filter(category__name__iexact=category_name).order_by('-created_at')

    return render(request, 'blog/home.html', {
        'articles': articles,
        'current_category': category_name.capitalize()
    })