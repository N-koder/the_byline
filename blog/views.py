from django.shortcuts import render, get_object_or_404, redirect
from .models import Article
from .forms import NewsletterForm
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render
from django.contrib import messages
from .models import ContactMessage
from django.conf import settings
from datetime import datetime
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect


@require_POST
def subscribe_newsletter(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Thank you for subscribing!")
    else:
        messages.error(request, "Please enter a valid email.")
    
    # Redirect back to the referring page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def home(request, category_slug=None):

    current_date = datetime.now().strftime("%A, %B %d, %Y")
      # You can add a success message with Django messages framework

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

 

    context = {
        'articles': articles,
        'featured_articles': featured_articles,
        'crick_key' : settings.RAPIDAPI_KEY,
        'opinion_articles': opinion_articles,
        'current_category': category_slug.capitalize() if category_slug else None,
        'current_date' : current_date
    }
    return render(request, 'blog/home.html', context)


def article_detail(request, slug):
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'blog/article_detail.html', {'article': article , 'current_date' : current_date})


def category_articles(request, category_name):
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    articles = Article.objects.filter(category__name__iexact=category_name).order_by('-created_at')
   

    return render(request, 'blog/home.html', {
        'articles': articles,
        'current_category': category_name.capitalize(),
        'current_date' : current_date
    })


def contact(request):
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    if request.method == 'POST':
        ContactMessage.objects.create(
            first_name=request.POST.get('first-name'),
            last_name=request.POST.get('last-name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        messages.success(request, "Thank you for contacting us. We'll get back to you soon!")
    
    return render(request, 'blog/contact.html' , {'current_date' : current_date}) 