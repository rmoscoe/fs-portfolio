from django.db.models import F
from django.views.generic import TemplateView
from .models import Experience, Education, SkillCategory
from .utils import sort_as_linked_list

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

class ResumeView(TemplateView):
    template_name = 'resume.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume_url'] = 'https://ryanmoscoe-portfolio.s3.us-west-1.amazonaws.com/Ryan+Moscoe+Resume.docx'
        context['experiences'] = Experience.objects.prefetch_related('roles', 'accomplishments').order_by(F('roles__end_date').desc(nulls_first=True))
        context['educations'] = Education.objects.all().order_by(F('graduation_date').desc(nulls_first=True))
        skill_categories = SkillCategory.objects.prefetch_related('skills')
        sorted_skill_categories = sort_as_linked_list(skill_categories)
        for category in sorted_skill_categories:
            category.sorted_skills = sort_as_linked_list(category.skills.all())
        context['skill_categories'] = sorted_skill_categories
        return context