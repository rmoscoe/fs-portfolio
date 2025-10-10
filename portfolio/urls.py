from django.views.decorators.cache import cache_page
from django.urls import path
from .views import SoftwareEngineeringView, PromptEngineeringView, InstructionalDesignView

urlpatterns = [
    path('software-engineering/', cache_page(24 * 60 * 60)(SoftwareEngineeringView.as_view()), name='software'),
    path('ai-prompt-engineering/', cache_page(24 * 60 * 60)(PromptEngineeringView.as_view()), name='ai'),
    path('instructional-design/', cache_page(24 * 60 * 60)(InstructionalDesignView.as_view()), name='instructional-design')
]