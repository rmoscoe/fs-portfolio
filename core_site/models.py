from django.db import models
from django.utils import timezone
from .utils import send_email

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
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    show = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        event_type = 'create' if self.last_modified is None else 'modify'
        event = event_type + ' portfolio item'
        email_data = Email.objects.get(event=event)
        model_name = self._meta.verbose_name.title()
        email_properties = {}
        match event_type:
            case 'create':
                email_properties['subject'] = email_data.subject.format(model_name=model_name)
                item_properties = [f'{k.replace("_", " ").title()}: {v}' for k, v in self.__dict__.items()]
                details = '\n'.join(item_properties)
                email_properties['body'] = email_data.body.format(model_name=model_name, details=details)
            case 'modify':
                vowels = 'AEIOU'
                article = 'An' if model_name[0] in vowels else 'A'
                article_and_model = f'{article} {model_name}'
                old = self.__class__.objects.get(pk=self.id).__dict__
                properties = list(old.keys())
                details = ''
                for prop in properties:
                    changed = 'Yes' if old.get(prop) != getattr(self, prop) else ''
                    details += f'<tr><td style="border-width:1px; border-color:#000000; border-style:solid;">{prop.replace('_', ' ').title()}</td><td style="border-width:1px; border-color:#000000; border-style:solid;">{old.get(prop)}</td><td style="border-width:1px; border-color:#000000; border-style:solid;">{getattr(self, prop)}</td><td style="border-width:1px; border-color:#000000; border-style:solid;">{changed}</td></tr>'
                email_properties['subject'] = email_data.subject.format(model_name=model_name, id=self.id)
                email_properties['body'] = email_data.body.format(article_and_model=article_and_model, details=details)
                email_properties['content_subtype'] = 'html'
        send_email(**email_properties)
        super().save(*args, **kwargs)

    
    def delete(self, *args, **kwargs):
        email_data = Email.objects.get(event='delete portfolio item')
        model_name = self._meta.verbose_name.title()
        vowels = 'AEIOU'
        article = 'An' if model_name[0] in vowels else 'A'
        article_and_model = f'{article} {model_name}'
        item_properties = [f'{k.replace("_", " ").title()}: {v}' for k, v in self.__dict__.items()]
        details = '\n'.join(item_properties)
        email_properties = {
            'subject': email_data.subject.format(model_name=model_name, id=self.id),
            'body': email_data.body.format(article_and_model=article_and_model, details=details)
        }
        send_email(**email_properties)
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return getattr(self, 'name', None) or getattr(self, 'employer', None) or getattr(self, 'title', None) or getattr(self, 'institution', None) or getattr(self, 'description', '')[:30] or str(type(self))
    
    class Meta:
        abstract = True


######################################
#           CORE MODELS              #
######################################

class Email(models.Model):
    event = models.CharField(max_length=255, help_text='The event that triggers the email and the name of the email')
    to = models.JSONField(null=True, blank=True, help_text='A list or tuple of email addresses, defaults to `(ryan@ryanmoscoe.com,)`')
    from_email = models.EmailField(null=True, blank=True, help_text='Defaults to settings.DEFAULT_FROM_EMAIL')
    reply_to = models.JSONField(null=True, blank=True, help_text='A list or tuple of email addresses, defaults to None')
    subject = models.CharField(max_length=255, help_text='The Subject line for the email')
    body = models.TextField(help_text='The email message body')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event', '-created_at']

class BlockedEmailAddress(models.Model):
    address = models.EmailField(null=True, blank=True, help_text='Option 1: enter a full email address')
    domain = models.CharField(max_length=255, null=True, blank=True, help_text='Option 2: Enter only a domain to block all addresses on that domain')

    class Meta:
        ordering = ['domain', 'address']

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

    class Meta:
        verbose_name_plural = 'Skill Categories'

class Skill(BasePortfolioModel):
    category = models.ForeignKey(SkillCategory, on_delete=models.PROTECT, related_name='skills')
    name = models.CharField(max_length=255)
    show_after = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='show_before')
    icon_url = models.URLField(blank=True, null=True)
    icon_img = models.FileField(blank=True, null=True, upload_to='images/')
    invert_icon = models.BooleanField(default=False)