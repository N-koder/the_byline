from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Article, Category,  Subscriber,ContactMessage


admin.site.register(Article)
admin.site.register(Category)
admin.site.register( Subscriber)
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'subject')
    ordering = ('-created_at',)
