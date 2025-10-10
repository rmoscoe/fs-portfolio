from django.contrib import admin
from django.db import models
from django.forms import widgets
from .models import *

# Register your models here.
class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ['last_modified']

class ModelWithURL(admin.ModelAdmin):
    formfield_overrides = {
        models.URLField: {
            'widget': widgets.TextInput
        }
    }

class BaseModelWithURLAdmin(BaseModelAdmin):
    formfield_overrides = {
        models.URLField: {
            'widget': widgets.TextInput
        }
    }

class ExperienceAdmin(BaseModelAdmin):
    fields = ['employer', 'city', 'state_province', 'remote', 'created_at', 'last_modified', 'show']
    list_display = ['employer', 'city', 'state_province', 'title', 'start_date', 'end_date', 'accomplishments']
    search_fields = ['employer', 'city', 'state_province']

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

class RoleAdmin(BaseModelAdmin):
    fields = ['experience', 'title', 'contract', 'start_date', 'end_date', 'created_at', 'last_modified', 'show']
    list_display = ['title', 'experience__employer', 'contract', 'start_date', 'end_date']
    search_fields = ['title']

class AccomplishmentAdmin(BaseModelAdmin):
    fields = ['experience', 'description', 'created_at', 'last_modified', 'show']
    list_display = ['experience__employer', 'description', 'show']
    search_fields = ['description']

class EducationAdmin(BaseModelAdmin):
    fields = ['institution', 'city', 'state_province', 'degree', 'field_of_study', 'graduation_date', 'created_at', 'last_modified', 'show']
    list_display = ['institution', 'degree', 'field_of_study', 'graduation_date']
    search_fields = ['institution', 'field_of_study']

class SkillCategoryAdmin(BaseModelAdmin):
    fields = ['name', 'show_after', 'created_at', 'last_modified', 'show']
    list_display = ['name', 'show_after', 'skills']
    search_fields = ['name', 'skills']

    def skills(self, obj):
        return ', '.join([skill.name for skill in obj.skills.all()])

class SkillAdmin(BaseModelWithURLAdmin):
    fields = ['category', 'name', 'show_after', 'icon_url', 'icon_img', 'invert_icon', 'created_at', 'last_modified', 'show']
    list_display = ['name', 'category__name', 'show_after__name', 'show']
    search_fields = ['name', 'icon_url']

class EmailAdmin(admin.ModelAdmin):
    fields = ['event', 'to', 'from_email', 'reply_to', 'subject', 'body', 'created_at', 'last_modified']
    readonly_fields = ['created_at', 'last_modified']
    list_display = ['event', 'from_email', 'subject', 'created_at', 'last_modified']
    search_fields = ['event', 'from_email', 'subject', 'body']


admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Accomplishment, AccomplishmentAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(SkillCategory, SkillCategoryAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Email, EmailAdmin)