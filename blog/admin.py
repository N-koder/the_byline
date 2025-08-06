from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE
from .models import Article, Category, Subscriber, ContactMessage

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_featured', 'is_opinion', 'created_at', 'image_preview', 'author_image_preview')
    list_filter = ('category', 'is_featured', 'is_opinion', 'created_at')
    search_fields = ('title', 'author', 'summary', 'body')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'image_preview', 'author_image_preview')
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'body':
            kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 30})
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'summary', 'body', 'author')
        }),
        ('Images', {
            'fields': ('image', 'image_preview', 'authorImage', 'author_image_preview'),
            'classes': ('collapse',)
        }),
        ('Categorization', {
            'fields': ('category', 'is_featured', 'is_opinion')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image and obj.image.url:
            try:
                return format_html(
                    '<img src="{}" style="max-height: 50px; max-width: 50px; border: 1px solid #ddd; border-radius: 4px;" alt="Article Image" />',
                    obj.image.url
                )
            except:
                return "Image error"
        return "No image"
    image_preview.short_description = 'Article Image'
    image_preview.allow_tags = True
    
    def author_image_preview(self, obj):
        if obj.authorImage and obj.authorImage.url:
            try:
                return format_html(
                    '<img src="{}" style="max-height: 50px; max-width: 50px; border: 1px solid #ddd; border-radius: 4px;" alt="Author Image" />',
                    obj.authorImage.url
                )
            except:
                return "Image error"
        return "No image"
    author_image_preview.short_description = 'Author Image'
    author_image_preview.allow_tags = True

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'subject')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
