from django.db.models import Count
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Topic, Post, UniquePageView, Like

class TopicList(ListView):
    model = Topic
    template_name = 'topics.html'

    def get_queryset(self):
        return Topic.objects.filter(parent=None)
    
class TopicDetail(DetailView):
    model = Topic
    template_name = 'topic.html'

    def get_queryset(self):
        return Topic.objects.select_related('parent').prefetch_related('children', 'posts').annotate(unique_page_views = Count('posts__uniquepageview', distinct=True), likes=Count('posts__like', distinct=True))

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'

    def get_queryset(self):
        return Post.objects.select_related('topic').prefetch_related('likes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = self.request.META.get('REMOTE_ADDR')
        post = self.object
        UniquePageView.objects.get_or_create(post=post, ip_address=ip)
        context['unique_page_views'] = post.uniquepageview_set.count()
        context['liked'] = post.like_set.filter(ip_address=ip).exists()
        context['likes'] = post.like_set.count()
        return context

class LikeView(View):
    def post(self, request):
        try:
            ip = request.META.get('REMOTE_ADDR')
            post_id = request.POST.get('post_id')
        except Exception as e:
            return HttpResponse(str(e), status_code=400)
        try:
            Like.objects.get_or_create(post=post_id, ip_address=ip)
        except Exception as e:
            return HttpResponse(str(e), status_code=500)
        return HttpResponse('Yay! You like my content.', status_code=200)
    
    def delete(self, request):
        try:
            ip = request.META.get('REMOTE_ADDR')
            post_id = request.POST.get('post_id')
        except Exception as e:
            return HttpResponse(str(e), status_code=400)
        try:
            Like.objects.get(post=post_id, ip_address=ip).delete()
            likes = len(Like.objects.filter(post=post_id))
        except Exception as e:
            return HttpResponse(str(e), status_code=500)
        return HttpResponse(f'Successfully deleted Like.::Likes Remaining: {likes}', status_code=200)