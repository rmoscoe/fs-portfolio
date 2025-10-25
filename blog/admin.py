from core_site.admin import BaseModelAdmin, BaseModelWithURLAdmin
from django.contrib import admin
from .models import Topic, Post, UniquePageView, Like

class TopicAdmin(BaseModelAdmin):
    fields = ['name', 'parent', 'show']
    list_display = ['name', 'parent__name', 'children', 'show', 'posts']
    search_fields = ['name']
    
    def children(self, obj):
        return '; '.join([child.name for child in obj.children.all()])
    
    def posts(self, obj):
        return '\n'.join([post.title for post in obj.posts.all()])

class PostAdmin(BaseModelWithURLAdmin):
    fields = ['topic', 'title', 'created_at', 'show', 'hero_image', 'hero_image_url', 'hero_image_alt', 'image_credit_text', 'image_credit_url', 'body']
    list_display = ['topic__name', 'title', 'created_at', 'show']
    search_fields = ['title', 'body']

class InteractionAdmin(admin.ModelAdmin):
    fields = ['post', 'ip_address', 'created_at']
    list_display = ['post', 'ip_address', 'created_at']
    search_fields = ['post', 'ip_address']

admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UniquePageView, InteractionAdmin)
admin.site.register(Like, InteractionAdmin)