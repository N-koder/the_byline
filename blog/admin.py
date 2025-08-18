from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE
from .models import Article, Category,  Subcategory, Subscriber, ContactMessage
# from django.core.exceptions import PermissionDenied

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_featured', 'is_opinion', 'created_at', 'image_preview', 'author_image_preview' , 'status')
    list_filter = ('status' ,'category', 'tags' , 'is_featured', 'is_opinion', 'created_at')
    search_fields = ('title', 'author', 'summary', 'body')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'image_preview', 'author_image_preview')
    actions = ["make_published", "make_draft"]

    def colored_status(self, obj):
        """Show colored status in Admin"""
        if obj.status == "published":
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', obj.status)
        return format_html('<span style="color: red; font-weight: bold;">{}</span>', obj.status)
    colored_status.admin_order_field = "status"
    colored_status.short_description = "Status"

    def make_published(self, request, queryset):
        updated = queryset.update(status="published")
        self.message_user(request, f"{updated} articles marked as Published ✅")
    make_published.short_description = "Mark selected as Published"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('blog.can_publish'):
            if 'make_published' in actions:
                del actions['make_published']
        return actions

    # def save_model(self, request, obj, form, change):
    #     """Prevent unauthorized users from publishing"""
    #     if obj.status == "published" and not request.user.has_perm("blog.can_publish"):
    #         raise PermissionDenied("🚫 You don’t have permission to publish articles.")
    #     super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm("blog.can_publish"):
            # Only show "Draft" to unauthorized users
            form.base_fields["status"].choices = [
                choice for choice in form.base_fields["status"].choices if choice[0] == "draft"
            ]
        return form

    def make_draft(self, request, queryset):
        updated = queryset.update(status="draft")
        self.message_user(request, f"{updated} articles marked as Draft 📝")
    make_draft.short_description = "Mark selected as Draft"
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'body':
            kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 30})
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'summary', 'body', 'author' , 'status')
        }),
        ('Images', {
            'fields': ('image', 'image_preview', 'authorImage', 'author_image_preview' , 'image_credit'),
            'classes': ('collapse',)
        }),
        ('Categorization', {
            'fields': ('category', 'subcategory' ,'tags' , 'is_featured', 'is_opinion')
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
    
@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
