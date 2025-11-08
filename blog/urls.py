from django.urls import path
from . import views

urlpatterns = [
    path('', views.TopicList.as_view(), name='blog'),
    path('topics/<pk>/', views.TopicDetail.as_view(), name='topic-detail'),
    path('topics/<topic_id>/posts/<pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('topics/<topic_id>/posts/<post_id>/like/', views.LikeView.as_view(), name='like')
]