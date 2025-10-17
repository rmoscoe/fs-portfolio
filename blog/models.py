from core_site.models import BasePortfolioModel
from django.db import models

class Topic(BasePortfolioModel):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)

    def __str__(self):
        return f'Topic: {self.name}'

    class Meta:
        ordering = ['name']

class Post(BasePortfolioModel):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    hero_image = models.FileField(upload_to='images/', blank=True, null=True)
    hero_image_url = models.URLField(blank=True, null=True)
    body = models.TextField()

    def __str__(self):
        return f'Post: {self.title}'
    
    class Meta:
        ordering = ['-created_at']

class Interaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'ip_address')
        abstract = True

class UniquePageView(Interaction):
    pass

class Like(Interaction):
    pass