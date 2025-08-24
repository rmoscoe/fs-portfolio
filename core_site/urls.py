from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), nam='about'),
    path('resume/', views.ResumeView.as_view(), name='resume'),
    path('contact/', views.ContactView.as_view(), name='contact')
]