from django.contrib import admin
from django.db import models
from django.forms import widgets
from .models import *

# Register your models here.
class InlineWithURL(admin.StackedInline):
    formfield_overrides = {
        models.URLField: {
            'widget': widgets.TextInput
        }
    }

class ModelWithURL(admin.ModelAdmin):
    formfield_overrides = {
        models.URLField: {
            'widget': widgets.TextInput
        }
    }

class RoleInline(admin.StackedInline):
    model = Role
    extra = 1
    fk_name = 'experience'

class AccomplishmentInline(admin.StackedInline):
    model = Accomplishment
    extra = 1
    fk_name = 'experience'

class ExperienceAdmin(admin.ModelAdmin):
    fields = ['employer', 'city', 'state_province', 'remote', 'created_at', 'last_modified', 'show']
    list_display = ['employer', 'city', 'state_province', 'title', 'start_date', 'end_date', 'accomplishments']
    search_fields = ['employer', 'city', 'state_province', 'roles__title', 'accomplishments__description']
    inlines = [RoleInline, AccomplishmentInline]

    def title(self, obj):
        first = obj.roles.first()
        return first.title if first else ''
    
    def start_date(self, obj):
        start_dates = [role.start_date for role in obj.roles.all() if role.start_date]
        if len(start_dates) > 0:
            return min(start_dates)
        return None
    
    def end_date(self, obj):
        end_dates = [role.end_date for role in obj.roles.all()]
        if None in end_dates or len(end_dates) == 0:
            return None
        return max(end_dates)

    def accomplishments(self, obj):
        return ', '.join([ac.description for ac in obj.accomplishments.all()])

class EducationAdmin(admin.ModelAdmin):
    fields = ['institution', 'city', 'state_province', 'degree', 'field_of_study', 'graduation_date', 'created_at', 'last_modified', 'show']
    list_display = ['institution', 'degree', 'field_of_study', 'graduation_date']
    search_fields = ['institution', 'field_of_study']

class SkillInline(InlineWithURL):
    model = Skill
    extra = 1
    fk_name = 'category'

class SkillCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'show_after', 'skills__name', 'skills__show_after', 'skills__icon_url', 'created_at', 'last_modified', 'show']
    list_display = ['name', 'show_after', 'skills']
    search_fields = ['name', 'skills']
    inlines = [SkillInline]

    def skills(self, obj):
        return ', '.join([skill.name for skill in obj.skills.all()])

class EmailAdmin(admin.ModelAdmin):
    fields = ['event', 'to', 'from_email', 'reply_to', 'subject', 'body', 'created_at', 'last_modified']
    list_display = ['event', 'from_email', 'subject', 'created_at', 'last_modified']
    search_fields = ['event', 'from_email', 'subject', 'body']


admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(SkillCategory, SkillCategoryAdmin)
admin.site.register(Email, EmailAdmin)