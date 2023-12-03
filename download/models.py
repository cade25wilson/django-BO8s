from django.db import models

# Create your models here.

class Video(models.Model):
    filename = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title