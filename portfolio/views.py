from core_site.models import SkillCategory, Skill
from core_site.utils import sort_as_linked_list
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy
from django.views.generic import TemplateView
import json
import logging
from .models import Project

logger = logging.getLogger('portfolio')
logger.setLevel(logging.DEBUG)

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
        logger.debug('Getting Context Data...')
        def sort_skill(skill):
            return skill.name

        try:
            context = super().get_context_data(**kwargs)
            logger.debug(f'Context: {context}')
            categories = SkillCategory.objects.all()
            logger.debug(f'Categories: {categories}')
            sorted_categories = sort_as_linked_list(categories)
            logger.debug(f'Sorted Categories: {sorted_categories}')
            project_category = getattr(self, 'project_category', 'software_engineering') or 'software_engineering'
            project_query_filters = {
                'show': True,
                project_category: True
            }
            projects = Project.objects.filter(**project_query_filters).prefetch_related('tech_stack')
            logger.debug(f'PROJECTS: {projects}')
            classroom_projects = Project.objects.filter(show=True, classroom=True).prefetch_related('tech_stack', 'course_materials') if project_category == 'elearning' else None
            if classroom_projects is not None:
                logger.debug(f'CLASSROOM PROJECTS: {classroom_projects}')
            sorted_projects = sort_as_linked_list(projects)
            logger.debug(f'SORTED PROJECTS: {sorted_projects}')
            project_groups = [sorted_projects]
            if classroom_projects:
                sorted_classroom_projects = sort_as_linked_list(classroom_projects)
                logger.debug('SORTED CLASSROOM PROJECTS: {sorted_classroom_projects}')
                project_groups.append(sorted_classroom_projects)
            filter_categories = getattr(self, 'filter_categories', [])
            filters = { filter_category: { 'icon_class': FILTER_ICON_CLASSES.get(filter_category, 'fa-solid fa-filter'), 'options': [] } for filter_category in filter_categories }
            logger.debug(f'filter_categories')
            context_keys = ['elearning_projects', 'classroom_projects'] if project_category == 'elearning' else ['projects']
            scope_options = []
            for i, project_group in enumerate(project_groups):
                logger.debug(f'Preparing Project Group {i}')
                context_projects = []
                for project in project_group:
                    logger.debug(f'Preparing Project {project}')
                    logger.debug(f'Identifying filters...')
                    if 'team' in filter_categories:
                        if project.team not in filters['team']['options']:
                            filters['team']['options'].append(project.team)
                    if 'scope' in filter_categories:
                        if project.scope not in filters['scope']['options']:
                            scope_options.append(project.scope)
                    if 'starter_code' in filter_categories:
                        if project.starter_code not in filters['starter_code']['options']:
                            filters['starter_code']['options'].append(project.starter_code)
                    logger.debug('Sorting tech stack')
                    sorted_tech_stack = []
                    for category in sorted_categories:
                        logger.debug(f'Sorting category: {category}')
                        category_skills = []
                        if 'tech_stack' in filter_categories:
                            for skill in category.skills.all():
                                if skill in project.tech_stack.all():
                                    logger.debug(f'Preparing skill {skill}')
                                    category_skills.append(skill)
                                    if skill not in filters['tech_stack']['options']:
                                        filters['tech_stack']['options'].append(skill)
                            logger.debug(f'Sorting category skills as linked list: {category_skills}')
                            sorted_category_skills_all = sort_as_linked_list(list(category.skills.all()))
                            sorted_category_skills = [skill for skill in sorted_category_skills_all if skill in category_skills]
                            logger.debug(f'Sorted Category Skills: {sorted_category_skills}\nDict-ifying sorted skills')
                            category_skills_list = []
                            for skill in sorted_category_skills:
                                skill_dict = skill.__dict__
                                skill_dict.pop('_state')
                                skill_dict['icon_img'] = skill.icon_img.url if skill.icon_img else ''
                                logger.debug(f'SKILL: {skill_dict}')
                                category_skills_list.append(skill_dict)
                            sorted_tech_stack.extend(category_skills_list)
                    logger.debug(f'SORTED TECH STACK: {sorted_tech_stack}')
                    if 'type' in filter_categories:
                        if project.classroom and 'Classroom' not in filters['type']['options']:
                            filters['type']['options'].append('Classroom')
                        if project.elearning and 'eLearning' not in filters['type']['options']:
                            filters['type']['options'].append('eLearning')
                    logger.debug(f'Dictifying project: {project}')
                    context_project = project.__dict__
                    context_project['tech_stack'] = sorted_tech_stack
                    context_project['image'] = project.image.url if project.image else ''
                    if project_category == 'elearning' and i == 1:
                        sorted_course_materials = [material for material in sort_as_linked_list(project.course_materials.all()) if material.show]
                        logger.debug(f'SORTED COURSE MATERIALS: {sorted_course_materials}')
                        material_dicts = []
                        for material in sorted_course_materials:
                            logger.debug(f'Dictifying material: {material}')
                            material_dict = material.__dict__
                            material_dict.pop('_state')
                            material_dict['image'] = material.image.url
                            logger.debug(f'MATERIAL DICT: {material_dict}')
                            material_dicts.append(material_dict)
                        context_project['sorted_course_materials'] = material_dicts
                    context_project.pop('_state')
                    context_project.pop('_prefetched_objects_cache')
                    logger.debug(f'CONTEXT PROJECT: {context_project}')
                    context_projects.append(context_project)
                context[context_keys[i]] = json.dumps(context_projects, cls=DjangoJSONEncoder)
                logger.debug(f'context[{context_keys[i]}]: {context[context_keys[i]]}')
            if 'tech_stack' in filter_categories:
                logger.debug('Sorting tech stack options...')
                filters['tech_stack']['options'].sort(key=sort_skill)
            if 'team' in filter_categories:
                logger.debug('Sorting team options...')
                filters['team']['options'].sort(reverse=True)
            if 'scope' in filter_categories:
                logger.debug('Preparing scope options...')
                for s in [None, 'Front End', 'Back End', 'Full Stack']:
                    if s in scope_options:
                        filters['scope']['options'].append(s)
            if 'starter_code' in filter_categories:
                logger.debug('Sorting starter_code options...')
                filters['starter_code']['options'].sort(reverse=True)
            if 'type' in filter_categories:
                logger.debug('Sorting type options...')
                filters['type']['options'].sort()
            context['filters'] = filters
            context['title'] = getattr(self, 'page_title', 'Portfolio') or 'Portfolio'
            context['sort_details'] = {
                'icon_class': 'fa-solid fa-sort',
                'options': ['Default', 'A-Z', 'Z-A', 'Newest']
            }
            logger.debug('Returning context...')
        except Exception as error:
            logger.debug(f'ERROR: {str(error)}')
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