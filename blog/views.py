from django.shortcuts import render, get_object_or_404, redirect
from .models import Article
from .forms import NewsletterForm
from django.contrib import messages
from django.db.models import Q

def home(request, category_slug=None):
    # Handle Newsletter Signup POST
    form = NewsletterForm()
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # You can add a success message with Django messages framework

    # Fetch articles
    articles = Article.objects.all().order_by('-created_at')
    featured_articles = Article.objects.filter(is_featured=True).order_by('-created_at')[:5]
    opinion_articles = Article.objects.filter(is_opinion=True)[:3]

    query = request.GET.get('q')

    if query:
        articles = articles.filter(
            Q(title__icontains=query) or
            Q(summary__icontains=query) or
            Q(content__icontains=query)
        )

    form = NewsletterForm()
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing!")
            form = NewsletterForm()  # Reset form

    context = {
        'articles': articles,
        'featured_articles': featured_articles,
        'opinion_articles': opinion_articles,
        'current_category': category_slug.capitalize() if category_slug else None,
        'form': form
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
