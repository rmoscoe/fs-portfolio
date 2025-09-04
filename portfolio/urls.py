from django.urls import path
from .views import SoftwareEngineeringView, PromptEngineeringView, InstructionalDesignView

urlpatterns = [
    path('software-engineering/', SoftwareEngineeringView.as_view(), name='software'),
    path('ai-prompt-engineering/', PromptEngineeringView.as_view(), name='ai'),
    path('instructional-design/', InstructionalDesignView.as_view(), name='instructional-design')
]