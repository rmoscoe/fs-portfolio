from django.db import models

# Create your models here.
DEGREE_CHOICES = [
    ('Post-Doctoral Fellowship', 'Post-Doctoral Fellowship'),
    ('Ph.D.', 'Ph.D.'),
    ('Ed.D.', 'Ed.D.'),
    ('M.D.', 'M.D.'),
    ('J.D.', 'J.D.'),
    ('Doctorate', 'Doctorate'),
    ('M.F.A.', 'M.F.A.'),
    ('M.S.', 'M.S.'),
    ('M.Ed.', 'M.Ed.'),
    ('M.A.', 'M.A.'),
    ('M.B.A.', 'M.B.A.'),
    ('Master\'s', 'Master\'s'),
    ('B.F.A.', 'B.F.A.'),
    ('B.S.', 'B.S.'),
    ('B.A.', 'B.A.'),
    ('B.B.A.', 'B.B.A.'),
    ('Bachelor\'s', 'Bachelor\'s'),
    ('A.S.', 'A.S.'),
    ('A.A.', 'A.A.'),
    ('Associate\'s', 'Associate\'s'),
    ('Certificate', 'Certificate'),
    ('Diploma', 'Diploma')
]

class BasePortfolioModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    show = models.BooleanField(default=True)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
        # TODO: After setting up email functionality, override the save() method to send me a notification whenever an instance is created, modified, or deleted. Also, implement two-factor authentication for the admin interface.
    
    # def delete(self, *args, **kwargs):
    #     super().delete(*args, **kwargs)
        # Email myself about the deletion
    
    class Meta:
        abstract = True


######################################
#          WORK EXPERIENCE           #
######################################

class Experience(BasePortfolioModel):
    employer = models.CharField(max_length=255)
    city = models.CharField(max_length=127)
    state_province = models.CharField(max_length=2)
    remote = models.BooleanField(default=False)

class Role(BasePortfolioModel):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='roles')
    title = models.CharField(max_length=255)
    contract = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-end_date', '-start_date']

class Accomplishment(BasePortfolioModel):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='accomplishments')
    description = models.CharField(max_length=255)


########################################
#             EDUCATION                #
########################################

class Education(BasePortfolioModel):
    institution = models.CharField(max_length=255)
    city = models.CharField(max_length=127)
    state_province = models.CharField(max_length=2)
    degree = models.CharField(max_length=50, choices=DEGREE_CHOICES)
    field_of_study = models.CharField(max_length=255)
    graduation_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-graduation_date']


#########################################
#                SKILLS                 #
#########################################

class SkillCategory(BasePortfolioModel):
    name = models.CharField(max_length=255)
    show_after = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='show_before')

class Skill(BasePortfolioModel):
    category = models.ForeignKey(SkillCategory, on_delete=models.PROTECT, related_name='skills')
    name = models.CharField(max_length=255)
    show_after = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='show_before')
    icon_url = models.URLField(blank=True, null=True)