from django.views.decorators.cache import cache_page
from django.urls import path
from .views import SoftwareEngineeringView, InstructionalDesignView

urlpatterns = [
    path('software-engineering/', cache_page(24 * 60 * 60)(SoftwareEngineeringView.as_view()), name='software'),
    path('instructional-design/', cache_page(24 * 60 * 60)(InstructionalDesignView.as_view()), name='instructional-design')
]