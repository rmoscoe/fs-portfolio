from django import forms
from django.core.exceptions import ValidationError
from .models import Project, CourseMaterial

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['last_modified']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.__class__ == forms.widgets.URLInput:
                self.fields[field].widget = forms.TextInput()
    
    def clean(self):
        cleaned_data = super().clean()
        for field in cleaned_data:
            cleaned_data[field] = cleaned_data[field].strip() if isinstance(cleaned_data[field], str) else cleaned_data[field]
        if cleaned_data.get('image') and not cleaned_data.get('image_alt'):
            raise ValidationError("Image alt text is required when an image is provided.")
        if not any([cleaned_data.get('deployed_url'), cleaned_data.get('github_url'), cleaned_data.get('video_url')]):
            raise ValidationError("At least one of Deployed URL, GitHub URL, or Video URL must be provided.")
        if cleaned_data.get('software_engineering'):
            if not cleaned_data.get('scope'):
                raise ValidationError("Scope is required when Software Engineering is selected.")
            if not cleaned_data.get('starter_code'):
                raise ValidationError("Starter Code must be indicated when Software Engineering is selected.")
        if not any([cleaned_data.get('prompt_engineering'), cleaned_data.get('software_engineering'), cleaned_data.get('elearning'), cleaned_data.get('classroom')]):
            raise ValidationError("At least one category (Prompt Engineering, Software Engineering, eLearning, Classroom) must be selected.")
        return cleaned_data
    
class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        exclude = ['last_modified']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.__class__ == forms.widgets.URLInput:
                self.fields[field].widget = forms.TextInput()
    
    def clean(self):
        cleaned_data = super().clean()
        for field in cleaned_data:
            cleaned_data[field] = cleaned_data[field].strip() if isinstance(cleaned_data[field], str) else cleaned_data[field]
        return cleaned_data