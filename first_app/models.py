from django.db import models

# Create your models here.
class StoryModel(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    path = models.TextField()