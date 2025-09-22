from django.shortcuts import render, get_object_or_404, redirect
from .models import Article , Category , Subcategory, Subscriber, Podcast
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
from django.views.decorators.csrf import csrf_protect , csrf_exempt
from django.contrib.auth.decorators import login_required
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


# def category_articles(request, category_name):
#     current_date = datetime.now().strftime("%A, %B %d, %Y")
#     normalized_name = category_name.lower()
        
#     # Get the primary category object for page header/title
#     category = get_object_or_404(Category, name__iexact=category_name)
    
#     # Get all subcategories for this category
#     subcategories = category.subcategories.all()

#     # Build a query to get articles from this category and its subcategories
#     article_query = Q(category=category)
    
#     # If there are subcategories, include articles from those as well
#     if subcategories:
#         article_query |= Q(subcategory__in=subcategories)

    
#     articles = Article.objects.filter(article_query , status='published').order_by('-created_at')

#     featured = articles[0] if articles else None
#     others = articles[1:] if articles.count() > 1 else []

#     context = {
#         'category': category,
#         'subcategories': subcategories,
#         'featured': featured,
#         'others': others,
#         'current_category': category.name,
#         'current_date': current_date,
#          # Show category badge on cards for all category pages
#         'show_badges': True,
#     }
#     return render(request, 'blog/category.html', context)


def category_articles(request, category_name):
    print(f"DEBUG: category_articles called with category_name: {category_name}")
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    
    # First, try to find subcategories with the matching name
    print(f"DEBUG: Trying to find subcategories with name: {category_name}")
    subcategories = Subcategory.objects.filter(name__iexact=category_name)
    print(f"DEBUG: Found {subcategories.count()} subcategories with name {category_name}")
    
    if subcategories.exists():
        print(f"DEBUG: Found subcategories: {list(subcategories)}")
        # Fetch all articles for these subcategories
        articles = Article.objects.filter(
            subcategory__in=subcategories,
            status='published',
        ).order_by('-created_at').distinct()
        print(f"DEBUG: Found {articles.count()} articles for subcategories")
        
        # Create a mock category object with the subcategory name for page title
        from django.db.models import Model
        class MockCategory:
            def __init__(self, name):
                self.name = name
                
            def __str__(self):
                return self.name
        
        mock_category = MockCategory(category_name)
        
        context = {
            'category': mock_category,  # Use mock category with subcategory name for page title
            'subcategories': subcategories,
            'featured': articles[0] if articles else None,
            'others': articles[1:] if articles.count() > 1 else [],
            'current_category': category_name,  # Use the subcategory name for the page title
            'current_date': current_date,
            # Show category badge on cards for all category pages
            'show_badges': True,
        }
        return render(request, 'blog/category.html', context)
    
    # If no subcategories found, try to find a category
    print(f"DEBUG: No subcategories found, trying to find category with name: {category_name}")
    try:
        category = Category.objects.get(name__iexact=category_name)
        print(f"DEBUG: Found category: {category}")
        # Get all subcategories for this category
        subcategories = category.subcategories.all()
        print(f"DEBUG: Found subcategories: {subcategories}")
        
        # Build a query to get articles from this category and its subcategories
        article_query = Q(category=category)
        
        # If there are subcategories, include articles from those as well
        if subcategories:
            article_query |= Q(subcategory__in=subcategories)
        
        # Fetch all matching articles
        articles = Article.objects.filter(article_query, status='published').order_by('-created_at')
        print(f"DEBUG: Found {articles.count()} articles for category {category_name}")
        
        context = {
            'category': category,
            'subcategories': subcategories,
            'featured': articles[0] if articles else None,
            'others': articles[1:] if articles.count() > 1 else [],
            'current_category': category.name,
            'current_date': current_date,
            # Show category badge on cards for all category pages
            'show_badges': True,
        }
        return render(request, 'blog/category.html', context)
    except Category.DoesNotExist:
        print(f"DEBUG: Category {category_name} not found")
        # If neither category nor subcategory found, return 404
        from django.http import Http404
        raise Http404("Category or subcategory does not exist")

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



@csrf_exempt
@login_required
def autosave_draft(request):
    print("Autosave function called")
    try:
        if request.method == "POST":
            print("Autosave request received")
            # Fix: Remove the comma that was making article_id a tuple
            article_id = request.POST.get("id")
            title = request.POST.get("title", "")
            slug = request.POST.get("slug", "")
            summary = request.POST.get("summary", "")
            body = request.POST.get("body", "")
            author = request.POST.get("author", "")
            tags = request.POST.get("tags", "")  # Fix: This should be a string, not a list

        print(f"Article ID: {article_id}")
        print(f"Title: {title}")
        print(f"Summary :  {summary}")
        print(f"Author: {author}")

        # Handle the case where we're updating an existing article
        if article_id:
  
            try:
                article = Article.objects.get(id=article_id)
                    # Don't overwrite slug unless explicitly changed
                if 'slug' not in request.POST or not request.POST['slug']:
                    del request.POST['slug']
                print(f"Updating existing article with ID: {article_id}")
                article.title = title
                article.slug = slug
                article.summary = summary
                article.body = body
                article.author = author
                article.status = "draft"
                article.save()
                print(f"Article updated successfully with ID: {article.id}")
                
                # Handle tags properly
                if tags:
                    article.tags.set([t.strip() for t in tags.split(',') if t.strip()])
                else:
                    article.tags.clear()
                    
            except Article.DoesNotExist:
                print(f"Article with ID {article_id} not found")
                return JsonResponse({"status": "error", "message": "Article not found"}, status=404)
        else:
            # Creating a new article
            print("Creating new article")
            article = Article.objects.create(
                title=title,
                slug=slug,
                summary=summary,
                body=body,
                author=author,
                status="draft"
            )
            print(f"New article created with ID: {article.id}")
            
            # Handle tags for new article
            if tags:
                article.tags.set([t.strip() for t in tags.split(',') if t.strip()])
            

        return JsonResponse({"status": "ok", "id": article.id})
    except Exception as e:
        print(f"Error in autosave_draft: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
        
    print("Invalid request method")


def podcast_list(request):
    episodes = Podcast.objects.filter(status='published')  # Only show published episodes
    query = request.GET.get('q')
    
    if query:
        episodes = Podcast.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(transcript__icontains=query),
            status='published'  # Ensure search also filters by published
        ).distinct()
    
    context = {
        'episodes': episodes,
        'search_query': query
    }
    return render(request, "blog/podcast_list.html", context)



def podcast_detail(request, slug):
    episode = get_object_or_404(Podcast, slug=slug, status='published')  # Only show published episodes
    return render(request, "blog/podcast_detail.html", {"episode": episode})


@csrf_exempt
@login_required
def save_podcast_draft(request):
    """
    Custom view for auto-saving podcast drafts in Django admin.
    """
    try:
        # Log received data for debugging
        print("Received podcast POST data:")
        for key, value in request.POST.items():
            print(f"  {key}: {value[:100]}{'...' if len(value) > 100 else ''} (length: {len(value)})")
        
        # Get the podcast ID from the request, if it exists
        podcast_id = request.POST.get('podcast_id')
        
        # Check if this is a new podcast or an existing one
        if podcast_id:
            # Editing existing podcast
            try:
                podcast = Podcast.objects.get(id=podcast_id)
            except Podcast.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Podcast not found'}, status=404)
        else:
            # Creating new podcast
            podcast = Podcast()
            
        # Update podcast fields from POST data
        field_mapping = {
            'title': 'title',
            'slug': 'slug',
            'description': 'description',
            # 'author': 'author',
        }
        
        # Update text fields
        for form_field, model_field in field_mapping.items():
            if form_field in request.POST:
                value = request.POST[form_field]
                print(f"Setting {model_field} to: {value[:100]}{'...' if len(value) > 100 else ''} (length: {len(value)})")
                setattr(podcast, model_field, value)
        
        # Handle status field
        if 'status' in request.POST:
            podcast.status = request.POST['status']
        elif not podcast.status:  # Set default status if not set
            podcast.status = 'draft'
            
        # Handle audio_link, youtube_embed and transcript
        if 'audio_link' in request.POST:
            podcast.audio_link = request.POST['audio_link']
        if 'youtube_embed' in request.POST:
            podcast.youtube_embed = request.POST['youtube_embed']
        if 'transcript' in request.POST:
            podcast.transcript = request.POST['transcript']
        
        # Save the podcast
        print(f"Saving podcast with title: {podcast.title}")
        podcast.save()
        print(f"Podcast saved with ID: {podcast.id}")
        
        return JsonResponse({
            'success': True,
            'podcast_id': podcast.id,
            'message': 'Draft saved successfully'
        })
        
    except Exception as e:
        print(f"Error saving podcast draft: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@login_required
def autosave_podcast_draft(request):
    print("Podcast autosave function called")
    try:
        if request.method == "POST":
            print("Podcast autosave request received")
            podcast_id = request.POST.get("id")
            title = request.POST.get("title", "")
            slug = request.POST.get("slug", "")
            description = request.POST.get("description", "")
            # author = request.POST.get("author", "")
            audio = request.POST.get("audio_link", "")
            youtube_link = request.POST.get("youtube_embed", "")
            transcript = request.POST.get("transcript", "")

            print(f"Podcast ID: {podcast_id}")
            print(f"Title: {title}")

            # Handle the case where we're updating an existing podcast
            if podcast_id:
                try:
                    podcast = Podcast.objects.get(id=podcast_id)
                    print(f"Updating existing podcast with ID: {podcast_id}")
                    podcast.title = title
                    podcast.slug = slug
                    podcast.description = description
                    # podcast.author = author
                    podcast.audio_link = audio
                    podcast.youtube_embed = youtube_link
                    podcast.transcript = transcript
                    podcast.status = "draft"
                    podcast.save()
                    print(f"Podcast updated successfully with ID: {podcast.id}")
                except Podcast.DoesNotExist:
                    print(f"Podcast with ID {podcast_id} not found")
                    return JsonResponse({"status": "error", "message": "Podcast not found"}, status=404)
            else:
                # Creating a new podcast
                print("Creating new podcast")
                podcast = Podcast.objects.create(
                    title=title,
                    slug=slug,
                    description=description,
                    # author=author,
                    audio_link = audio,
                    youtube_embed = youtube_link,
                    transcript=transcript,
                    status="draft"
                )
                print(f"New podcast created with ID: {podcast.id}")

            return JsonResponse({"status": "ok", "id": podcast.id})
    except Exception as e:
        print(f"Error in autosave_podcast_draft: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
    print("Invalid request method")

 
