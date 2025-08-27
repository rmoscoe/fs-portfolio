from core_site.models import BasePortfolioModel, Skill
from django.db import models

TEAM_CHOICES = [
    ('Solo', 'Solo'),
    ('Group', 'Group')
]

SCOPE_CHOICES = [
    ('FE', 'Front End'),
    ('BE', 'Back End'),
    ('FS', 'Full Stack'),
    (None, '')
]

class Project(BasePortfolioModel):
    name = models.CharField(max_length=80)
    image = models.ImageField(blank=True, null=True)
    image_alt = models.CharField(max_length=150, blank=True, null=True)
    deployed_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    description = models.TextField()
    tech_stack = models.ManyToManyField(Skill)
    team = models.CharField(max_length=10, choices=TEAM_CHOICES, default='Solo')
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, blank=True, null=True)
    starter_code = models.BooleanField(blank=True, null=True)
    show_after = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='show_before')
    prompt_engineering = models.BooleanField(default=False)
    software_engineering = models.BooleanField(default=False)
    elearning = models.BooleanField(default=False)
    classroom = models.BooleanField(default=False)

class CourseMaterial(BasePortfolioModel):
    name = models.CharField(max_length=80)
    image = models.ImageField()
    image_alt = models.CharField(max_length=150)
    deployed_url = models.URLField()
    show_after = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='show_before')
    course = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='course_materials')