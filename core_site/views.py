from . import forms
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
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
    
class ContactView(FormView):
    template_name = 'contact.html'
    form_class = forms.ContactForm
    success_url = reverse_lazy('contact')
    # success_message = 'Your message has been sent. Thank you for reaching out! I will respond within one business day.'

    def form_valid(self, form):
        if form.cleaned_data.get('email_success'):
            messages.success(self.request, 'Your message has been sent. Thank you for reaching out! I will respond within one business day.')
        else:
            messages.error(self.request, 'Your message could not be sent. Please try again or email me directly at ryan@ryanmoscoe.com.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Your message could not be sent. Please try again or email me directly at ryan@ryanmoscoe.com.')
        return super().form_invalid(form)