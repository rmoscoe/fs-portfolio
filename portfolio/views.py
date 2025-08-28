from core_site.models import SkillCategory, Skill
from core_site.utils import sort_as_linked_list
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import Project, CourseMaterial

class SoftwareEngineeringView(TemplateView):
    template_name = 'software.html'

    def get_context_data(self, **kwargs):
        def sort_skill(skill):
            return skill.name
        
        context = super().get_context_data(**kwargs)
        categories = SkillCategory.objects.all()
        sorted_categories = sort_as_linked_list(categories)
        projects = Project.objects.filter(show=True, software_engineering=True).prefetch_related('tech_stack')
        sorted_projects = sort_as_linked_list(projects)
        filters = {
            'tech_stack': [],
            'team': [],
            'scope': [],
            'starter_code': []
        }
        scope_options = []
        for project in sorted_projects:
            if project.team not in filters['team']:
                filters['team'].append(project.team)
            if project.scope not in filters['scope']:
                scope_options.append(project.scope)
            if project.starter_code not in filters['starter_code']:
                filters['starter_code'].append(project.starter_code)
            sorted_tech_stack = []
            for category in sorted_categories:
                category_skills = []
                for skill in category.skills.all():
                    if skill in project.tech_stack.all():
                        category_skills.append(skill)
                        if skill not in filters['tech_stack']:
                            filters['tech_stack'].append(skill)
                sorted_category_skills = sort_as_linked_list(category_skills)
                sorted_tech_stack.extend(sorted_category_skills)
            project.sorted_tech_stack = sorted_tech_stack
        context['projects'] = sorted_projects
        filters['tech_stack'].sort(key=sort_skill)
        filters['team'].sort(reverse=True)
        for s in [None, 'Front End', 'Back End', 'Full Stack']:
            if s in scope_options:
                filters['scope'].append(s)
        filters['starter_code'].sort(reverse=True)
        context['filters'] = filters
        return context

class PromptEngineeringView(TemplateView):
    template_name = 'ai.html'

    def get_context_data(self, **kwargs):
        def sort_skill(skill):
            return skill.name
        
        context = super().get_context_data(**kwargs)
        categories = SkillCategory.objects.all()
        sorted_categories = sort_as_linked_list(categories)
        projects = Project.objects.filter(show=True, prompt_engineering=True).prefetch_related('tech_stack')
        sorted_projects = sort_as_linked_list(projects)
        filters = {
            'tech_stack': [],
            'team': [],
            'scope': [],
            'starter_code': []
        }
        scope_options = []
        for project in sorted_projects:
            if project.team not in filters['team']:
                filters['team'].append(project.team)
            if project.scope and project.scope not in filters['scope']:
                scope_options.append(project.scope)
            if project.starter_code and project.starter_code not in filters['starter_code']:
                filters['starter_code'].append(project.starter_code)
            sorted_tech_stack = []
            for category in sorted_categories:
                category_skills = []
                for skill in category.skills.all():
                    if skill in project.tech_stack.all():
                        category_skills.append(skill)
                        if skill not in filters['tech_stack']:
                            filters['tech_stack'].append(skill)
                sorted_category_skills = sort_as_linked_list(category_skills)
                sorted_tech_stack.extend(sorted_category_skills)
            project.sorted_tech_stack = sorted_tech_stack
        context['projects'] = sorted_projects
        filters['tech_stack'].sort(key=sort_skill)
        filters['team'].sort(reverse=True)
        for s in [None, 'Front End', 'Back End', 'Full Stack']:
            if s in scope_options:
                filters['scope'].append(s)
        filters['starter_code'].sort(reverse=True)
        context['filters'] = filters
        return context
    
class InstructionalDesign(TemplateView):
    template_name = 'instructional_design.html'

    def get_context_data(self, **kwargs):
        def sort_skill(skill):
            return skill.name
        
        context = super().get_context_data(**kwargs)
        categories = SkillCategory.objects.all()
        sorted_categories = sort_as_linked_list(categories)
        classroom_projects = Project.objects.filter(show=True, classroom=True).prefetch_related('tech_stack', 'course_materials')
        elearning_projects = Project.objects.filter(show=True, elearning=True).prefetch_related('tech_stack', 'course_materials')
        sorted_classroom_projects = sort_as_linked_list(classroom_projects)
        sorted_elearning_projects = sort_as_linked_list(elearning_projects)
        filters = {
            'tech_stack': [],
            'team': [],
        }
        context_keys = ['classroom_projects', 'elearning_projects']
        for i, project_type in enumerate([sorted_classroom_projects, sorted_elearning_projects]):
            for project in project_type:
                if project.team not in filters['team']:
                    filters['team'].append(project.team)
                sorted_tech_stack = []
                for category in sorted_categories:
                    category_skills = []
                    for skill in category.skills.all():
                        if skill in project.tech_stack.all():
                            category_skills.append(skill)
                            if skill not in filters['tech_stack']:
                                filters['tech_stack'].append(skill)
                    sorted_category_skills = sort_as_linked_list(category_skills)
                    sorted_tech_stack.extend(sorted_category_skills)
                project.sorted_tech_stack = sorted_tech_stack
                project.sorted_course_materials = sort_as_linked_list(project.course_materials.filter(show=True))
            context[context_keys[i]] = project_type
        filters['tech_stack'].sort(key=sort_skill)
        filters['team'].sort(reverse=True)
        context['filters'] = filters
        return context