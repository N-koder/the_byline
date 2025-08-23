from django.shortcuts import render, get_object_or_404, redirect
from .models import Article , Category , Subscriber
from .forms import NewsletterForm
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render
from django.contrib import messages
from .models import ContactMessage
from django.conf import settings
from datetime import datetime
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, JsonResponse
from collections import OrderedDict
from django.template.loader import render_to_string
from django.utils.html import mark_safe
import re
from taggit.models import Tag
from django.contrib.auth.models import User

@require_POST
def subscribe_newsletter(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        # Check if email already exists
        if Subscriber.objects.filter(email=email).exists():
            messages.info(request, "You're already subscribed with this email!")
        else:
            try:
                form.save()
                # Store email in session
                # request.session['subscriber_email'] = subscriber.email
                messages.success(request, "Thank you for subscribing!")
            except Exception as e:
                # Handle any database errors
                messages.error(request, "An error occurred. Please try again.")
    else:
         # Check if it's a duplicate email error
        email = request.POST.get('email', '')
        if email and Subscriber.objects.filter(email=email).exists():
            messages.info(request, "You're already subscribed with this email!")
        else:
            messages.error(request, "Please enter a valid email.")
    
    # Redirect back to the referring page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# def ajax_search(request):
#     query = request.GET.get('q', '')
#     results = []

#     if query:
#         articles = Article.objects.filter(
#             Q(title__icontains=query) |
#             Q(summary__icontains=query) |
#             Q(body__icontains=query)
#         ).distinct()[:10]

#         html = render_to_string('blog/partials/search_results.html', {'articles': articles})
#         return JsonResponse({'html': html})

#     return JsonResponse({'html': ''})

def highlight_keyword(text, keyword):
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return mark_safe(pattern.sub(f'<mark class="bg-white text-gray-400">{keyword}</mark>', text))

# def home(request, category_slug=None):

#     current_date = datetime.now().strftime("%A, %B %d, %Y")
#       # You can add a success message with Django messages framework

#     # Fetch articles
#     articles = Article.objects.all().order_by('-created_at')
#     featured_articles = Article.objects.filter(is_featured=True).order_by('-created_at')[:5]
#     opinion_articles = Article.objects.filter(is_opinion=True)[:3]
    
#     categories = Category.objects.all()
#     category_articles = OrderedDict()

#     for category in categories:
#         cat_articles = Article.objects.filter(category=category).order_by('-created_at')[:4]
#         if cat_articles:
#             featured = cat_articles[0]
#             others = cat_articles[1:]
#             category_articles[category] = {
#                 'featured': featured,
#                 'others': others
#             }


#      # Search and/or filter
#     category = request.GET.get('category')
#     query = request.GET.get('q')

#     if category:
#         articles = articles.filter(category__name__iexact=category)

#     if query:
#         articles = articles.filter(
#             Q(title__icontains=query) or Q(summary__icontains=query) or Q(body__icontains=query)
#         )

#         # Optional: Highlight search terms
#         for a in articles:
#             a.title = highlight_keyword(a.title, query)
#             a.summary = highlight_keyword(a.summary, query)

 

#     context = {
#         'articles': articles,
#         'featured_articles': featured_articles,
#         'crick_key' : settings.RAPIDAPI_KEY,
#         'opinion_articles': opinion_articles,
#         'current_category': category_slug.capitalize() if category_slug else None,
#         'category_articles': category_articles,
#         'current_date' : current_date,
#     }
#     return render(request, 'blog/home.html', context)


def home(request, category_slug=None):
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    query = request.GET.get('q')
    categories = Category.objects.all()
    context = {
        'crick_key': settings.RAPIDAPI_KEY,
        'opinion_articles': Article.objects.filter(is_opinion=True, status='published').order_by('-created_at'),
        'featured_articles': Article.objects.filter(is_featured=True,  status='published').order_by('-created_at')[:7],
        'recent_articles': Article.objects.filter(status='published').order_by('-created_at')[:7],
        'current_category': category_slug.capitalize() if category_slug else None,
        'current_date': current_date
    }

    # 🔍 Handle search
    if query:
        search_articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(body__icontains=query)
        ).filter(status='published').order_by('-created_at').distinct()

        for a in search_articles:
            a.title = highlight_keyword(a.title, query)
            a.summary = highlight_keyword(a.summary, query)

        context['articles'] = search_articles
        context['search_query'] = query
        return render(request, 'blog/home.html', context)

    # 📰 Normal category sections (only if not searching)
    from collections import OrderedDict
    category_articles = OrderedDict()
    for category in categories:
        cat_articles = Article.objects.filter(category=category ,  status='published').order_by('-created_at')[:4]
        if cat_articles:
            featured = cat_articles[0]
            others = cat_articles[1:]
            category_articles[category] = {
                'featured': featured,
                'others': others
            }

    context['category_articles'] = category_articles
    return render(request, 'blog/home.html', context)

def article_detail(request, slug):
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    article = get_object_or_404(Article, slug=slug , status='published')
    return render(request, 'blog/article_detail.html', {'article': article , 'current_date' : current_date})


def tagged_articles(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    articles = Article.objects.filter(tags__in=[tag] , status='published').order_by('-created_at')
    context = {
        'articles': articles,
        'search_query': tag.name,
        'tag': tag
    }
    return render(request, 'blog/home.html', context)


def category_articles(request, category_name):
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    normalized_name = category_name.lower()
        
    # Get the primary category object for page header/title
    category = get_object_or_404(Category, name__iexact=category_name)
    
    # Get all subcategories for this category
    subcategories = category.subcategories.all()

    # Build a query to get articles from this category and its subcategories
    article_query = Q(category=category)
    
    # If there are subcategories, include articles from those as well
    if subcategories:
        article_query |= Q(subcategory__in=subcategories)

    
    articles = Article.objects.filter(article_query , status='published').order_by('-created_at')

    featured = articles[0] if articles else None
    others = articles[1:] if articles.count() > 1 else []

    context = {
        'category': category,
        'subcategories': subcategories,
        'featured': featured,
        'others': others,
        'current_category': category.name,
        'current_date': current_date,
         # Show category badge on cards for all category pages
        'show_badges': True,
    }
    return render(request, 'blog/category.html', context)

def author_articles(request, username):
    author = get_object_or_404(User, username=username)
    articles = Article.objects.filter(author=author , status='published').order_by("-created_at")
    
    context = {
        "author": author,
        "articles": articles,
    }
    return render(request, "blog/author_articles.html", context)


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


def about(request):
    # founders = Founder.objects.all()  # Optional: Create Founder model if dynamic
    # context = {
    #     'founders': founders
    # }
    return render(request, 'blog/about.html')

def privacy_policy(request):
    return render(request, 'blog/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'blog/terms_of_service.html')

def cookie_policy(request):
    return render(request, 'blog/cookie_policy.html')
