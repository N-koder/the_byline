from email.policy import default
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager

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
