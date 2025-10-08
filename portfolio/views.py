from core_site.models import SkillCategory, Skill
from core_site.utils import sort_as_linked_list
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy
from django.views.generic import TemplateView
import json
from .models import Project, CourseMaterial

FILTER_ICON_CLASSES = {
    'tech_stack': 'fa-solid fa-laptop-code',
    'team': 'fa-solid fa-people-group',
    'scope': 'fa-solid fa-crosshairs',
    'starter_code': 'fa-solid fa-square-binary',
    'type': 'fa-solid fa-list'
}

class TechProjectsMixin:
    filter_categories = ['tech_stack', 'team']

    def get_context_data(self, **kwargs):
        def sort_skill(skill):
            return skill.name

        context = super().get_context_data(**kwargs)
        categories = SkillCategory.objects.all()
        sorted_categories = sort_as_linked_list(categories)
        project_category = getattr(self, 'project_category', 'software_engineering') or 'software_engineering'
        project_query_filters = {
            'show': True,
            project_category: True
        }
        projects = Project.objects.filter(**project_query_filters).prefetch_related('tech_stack')
        classroom_projects = Project.objects.filter(show=True, classroom=True).prefetch_related('tech_stack', 'course_materials') if project_category == 'elearning' else None
        sorted_projects = sort_as_linked_list(projects)
        project_groups = [sorted_projects]
        if classroom_projects:
            sorted_classroom_projects = sort_as_linked_list(classroom_projects)
            project_groups.append(sorted_classroom_projects)
        filter_categories = getattr(self, 'filter_categories', [])
        filters = { filter_category: { 'icon_class': FILTER_ICON_CLASSES.get(filter_category, 'fa-solid fa-filter'), 'options': [] } for filter_category in filter_categories }
        context_keys = ['elearning_projects', 'classroom_projects'] if project_category == 'elearning' else ['projects']
        scope_options = []
        for i, project_group in enumerate(project_groups):
            context_projects = []
            for project in project_group:
                if 'team' in filter_categories:
                    if project.team not in filters['team']['options']:
                        filters['team']['options'].append(project.team)
                if 'scope' in filter_categories:
                    if project.scope not in filters['scope']['options']:
                        scope_options.append(project.scope)
                if 'starter_code' in filter_categories:
                    if project.starter_code not in filters['starter_code']['options']:
                        filters['starter_code']['options'].append(project.starter_code)
                sorted_tech_stack = []
                for category in sorted_categories:
                    category_skills = []
                    if 'tech_stack' in filter_categories:
                        for skill in category.skills.all():
                            if skill in project.tech_stack.all():
                                category_skills.append(skill)
                                if skill not in filters['tech_stack']['options']:
                                    filters['tech_stack']['options'].append(skill)
                        sorted_category_skills_all = sort_as_linked_list(list(category.skills.all()))
                        sorted_category_skills = [skill for skill in sorted_category_skills_all if skill in category_skills]
                        category_skills_list = []
                        for skill in sorted_category_skills:
                            skill_dict = skill.__dict__
                            skill_dict.pop('_state')
                            category_skills_list.append(skill_dict)
                        sorted_tech_stack.extend(category_skills_list)
                if 'type' in filter_categories:
                    if project.classroom and 'Classroom' not in filters['type']['options']:
                        filters['type']['options'].append('Classroom')
                    if project.elearning and 'eLearning' not in filters['type']['options']:
                        filters['type']['options'].append('eLearning')
                context_project = project.__dict__
                context_project['tech_stack'] = sorted_tech_stack
                context_project['image'] = project.image.url if project.image else ''
                if project_category == 'elearning' and i == 1:
                    sorted_course_materials = [material for material in sort_as_linked_list(project.course_materials.all()) if material.show]
                    material_dicts = []
                    for material in sorted_course_materials:
                        material_dict = material.__dict__
                        material_dict.pop('_state')
                        material_dict['image'] = material.image.url
                        material_dicts.append(material_dict)
                    context_project['sorted_course_materials'] = material_dicts
                context_project.pop('_state')
                context_project.pop('_prefetched_objects_cache')
                context_projects.append(context_project)
            context[context_keys[i]] = json.dumps(context_projects, cls=DjangoJSONEncoder)
        if 'tech_stack' in filter_categories:
            filters['tech_stack']['options'].sort(key=sort_skill)
        if 'team' in filter_categories:
            filters['team']['options'].sort(reverse=True)
        if 'scope' in filter_categories:
            for s in [None, 'Front End', 'Back End', 'Full Stack']:
                if s in scope_options:
                    filters['scope']['options'].append(s)
        if 'starter_code' in filter_categories:
            filters['starter_code']['options'].sort(reverse=True)
        if 'type' in filter_categories:
            filters['type']['options'].sort()
        context['filters'] = filters
        context['title'] = getattr(self, 'page_title', 'Portfolio') or 'Portfolio'
        context['sort_details'] = {
            'icon_class': 'fa-solid fa-sort',
            'options': ['Default', 'A-Z', 'Z-A', 'Newest']
        }
        return context

class SoftwareEngineeringView(TechProjectsMixin, TemplateView):
    template_name = 'projects.html'
    filter_categories = ['tech_stack', 'team', 'scope', 'starter_code']
    project_category = 'software_engineering'
    page_title = 'Software Engineering'

class PromptEngineeringView(TechProjectsMixin, TemplateView):
    template_name = 'projects.html'
    filter_categories = ['tech_stack', 'team', 'scope', 'starter_code']
    project_category = 'prompt_engineering'
    page_title = 'AI Prompt Engineering'
    
class InstructionalDesignView(TechProjectsMixin, TemplateView):
    template_name = 'instructional_design.html'
    filter_categories = ['tech_stack', 'team', 'type']
    project_category = 'elearning'
    page_title = 'Instructional Design'