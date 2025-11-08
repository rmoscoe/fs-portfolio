from django.db.models import Count, Prefetch
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
import json
from .models import Topic, Post, UniquePageView, Like

class TopicList(ListView):
    model = Topic
    template_name = 'topics.html'

    def get_queryset(self):
        queryset = Topic.objects.filter(parent=None)
        for topic in queryset:
            print(str(topic))
        return queryset
    
class TopicDetail(DetailView):
    model = Topic
    template_name = 'topic.html'

    def get_queryset(self):
        return Topic.objects.select_related('parent').prefetch_related('children', Prefetch('posts', queryset=Post.objects.annotate(unique_page_views=Count('uniquepageview'), likes=Count('like'))))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_url'] = reverse('blog')
        ancestors = []
        parent = self.object.parent
        while parent:
            parent_breacrumb = {
                'name': parent.name,
                'url': reverse('topic-detail', args=[parent.id])
            }
            ancestors.append(parent_breacrumb)
            parent = parent.parent
        context['ancestors'] = reversed(ancestors)
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'

    def get_queryset(self):
        return Post.objects.select_related('topic').prefetch_related('like_set', 'uniquepageview_set')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = self.request.META.get('REMOTE_ADDR')
        post = self.object
        cookie_name = f'post_{post.id}_viewed'
        has_view_cookie = cookie_name in self.request.COOKIES
        has_ip_view = UniquePageView.objects.filter(post=post, ip_address=ip).exists()
        context['set_view_cookie'] = False
        if not has_view_cookie:
            context['set_view_cookie'] = f'{cookie_name}=true; Path=/; Max-Age=31536000'
            if not has_ip_view:
                UniquePageView.objects.create(post=post, ip_address=ip)
        context['unique_page_views'] = post.uniquepageview_set.count()
        cookie_name = f'post_{post.id}_liked'
        has_like_cookie = cookie_name in self.request.COOKIES
        has_ip_like = Like.objects.filter(post=post, ip_address=ip).exists()
        context['set_like_cookie'] = False
        if not has_like_cookie and has_ip_like:
            context['set_like_cookie'] = f'{cookie_name}=true; Path=/; Max-Age=31536000'
        context['liked'] = has_like_cookie or has_ip_like
        context['likes'] = post.like_set.count()
        context['blog_url'] = reverse('blog')
        ancestors = []
        parent = post.topic
        while parent:
            parent_breacrumb = {
                'name': parent.name,
                'url': reverse('topic-detail', args=[parent.id])
            }
            ancestors.append(parent_breacrumb)
            parent = parent.parent
        context['ancestors'] = reversed(ancestors)
        return context

class LikeView(View):
    def post(self, request, topic_id, post_id):
        try:
            ip = request.META.get('REMOTE_ADDR')
            if not post_id:
                return HttpResponse('post_id is required.', status=400)
        except Exception as e:
            return HttpResponse(str(e), status=400)
        try:
            Like.objects.get_or_create(post_id=post_id, ip_address=ip)
            likes = Like.objects.filter(post=post_id).count()
        except Exception as e:
            return HttpResponse(str(e), status=500)
        return HttpResponse(f'{likes}', status=200)
    
    def delete(self, request, topic_id, post_id):
        try:
            ip = request.META.get('REMOTE_ADDR')
            if not post_id:
                return HttpResponse('post_id is required.', status=400)
        except Exception as e:
            return HttpResponse(str(e), status=400)
        try:
            Like.objects.get(post_id=post_id, ip_address=ip).delete()
            likes = Like.objects.filter(post=post_id).count()
        except Like.DoesNotExist:
            return HttpResponse('Like not found.', status=404)
        except Exception as e:
            return HttpResponse(str(e), status=500)
        return HttpResponse(f'{likes}', status=200)