from email.policy import default
from django.db import models
from django.utils import timezone

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager

from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Article(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    body = models.TextField()
    image = models.ImageField(upload_to='article_images/')
    image_credit = models.CharField(max_length=200, default='')
    authorImage = models.ImageField(upload_to='author_images/' , default='author_images/writer.jpg')
    author = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    is_opinion = models.BooleanField(default=False)

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft"
    )
    
    class Meta:
        permissions = [
            ("can_publish", "Can publish articles"),
        ]
        
    
    def __str__(self):
        return f"{self.title } ({self.status})"

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

from django.db import models

class ContactMessage(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.first_name} {self.last_name or ''} - {self.subject}"
        

class Podcast(models.Model):

    STATUS_CHOICES = (
        ("draft" , "Draft"),
        ("published" , "Published")
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    cover_image = models.ImageField(upload_to="podcasts/covers/")
    description = models.TextField()
    audio_file = models.FileField(upload_to="podcasts/audio/", blank=True, null=True)
    audio_link = models.URLField(blank=True, null=True)  
    youtube_embed = models.URLField(blank=True, null=True)  
    transcript = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    anecdote = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft"
    )
    
    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse("podcast_detail", kwargs={"slug": self.slug})



class ExternalFeed(models.Model):
    """
    Stores NewsVoir RSS feeds
    """
    provider = models.CharField(max_length=100, default="NewsVoir")
    url = models.URLField(unique=True)
    target_category = models.CharField(max_length=255)  # maps to your category
    is_active = models.BooleanField(default=True)
    last_fetched = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.provider} → {self.target_category}"


class PressRelease(models.Model):

    STATUS_CHOICES = (
        ("draft" , "Draft"),
        ("published" , "Published")
    )

    """
    Stores imported Press Releases separately from editorial articles
    """
    guid = models.CharField(max_length=500, unique=True) 
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True , max_length=300)
    summary = models.TextField(null=True, blank=True)
    # content = models.TextField()
    image = models.URLField(null=True, blank=True)
    image_credit = models.CharField(max_length=200, default='' ,blank=True)
    link = models.URLField(unique=True)  # original NewsVoir URL
    published_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )
    source = models.CharField(max_length=255, default="NewsVoir")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="press_releases",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("press_release_detail", args=[self.slug])
        
    def __str__(self):
        return self.title
