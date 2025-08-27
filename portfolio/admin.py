from django.contrib import admin
from .models import Project, CourseMaterial
from .forms import ProjectForm, CourseMaterialForm

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    list_display = ('name', 'show', 'prompt_engineering', 'software_engineering', 'elearning', 'classroom')
    ordering = ['-created_at', 'name']
    search_fields = ['name', 'description', 'tech_stack__name']

class CourseMaterialAdmin(admin.ModelAdmin):
    form = CourseMaterialForm
    list_display = ('name', 'show', 'course__name')
    ordering = ['course__name', '-created_at', 'name']
    search_fields = ['name', 'course__name']


admin.site.register(Project, ProjectAdmin)
admin.site.register(CourseMaterial, CourseMaterialAdmin)