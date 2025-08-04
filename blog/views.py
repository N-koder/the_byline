from django.shortcuts import render, get_object_or_404, redirect
from .models import Article , Category
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


# def ajax_search(request):
#     query = request.GET.get('q', '')
#     results = []

#     if query:
#         articles = Article.objects.filter(
#             Q(title__icontains=query) |
#             Q(summary__icontains=query) |
#             Q(content__icontains=query)
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
#             Q(title__icontains=query) or Q(summary__icontains=query) or Q(content__icontains=query)
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
        'opinion_articles': Article.objects.filter(is_opinion=True),
        'featured_articles': Article.objects.filter(is_featured=True).order_by('-created_at')[:5],
        'current_category': category_slug.capitalize() if category_slug else None,
        'current_date': current_date
    }

    # 🔍 Handle search
    if query:
        search_articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

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
        cat_articles = Article.objects.filter(category=category).order_by('-created_at')[:4]
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
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'blog/article_detail.html', {'article': article , 'current_date' : current_date})


def category_articles(request, category_name):
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    category = get_object_or_404(Category, name__iexact=category_name)
    articles = Article.objects.filter(category=category).order_by('-created_at')

    featured = articles[0] if articles else None
    others = articles[1:] if articles.count() > 1 else []

    context = {
        'category': category,
        'featured': featured,
        'others': others,
        'current_category': category.name,
        'current_date': current_date
    }
    return render(request, 'blog/category.html', context)


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