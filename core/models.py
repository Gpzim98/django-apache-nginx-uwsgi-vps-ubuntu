from django.db import models

class Movie(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='movies_pics')
