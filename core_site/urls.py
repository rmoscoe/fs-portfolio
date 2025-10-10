from django.views.decorators.cache import cache_page
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='about'),
    path('resume/', cache_page(24 * 60 * 60)(views.ResumeView.as_view()), name='resume'),
    path('contact/', views.ContactView.as_view(), name='contact')
]