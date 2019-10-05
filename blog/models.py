from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})

class tipOut(models.Model):
    teppan = models.CharField(max_length=140, default='0')
    sushi = models.CharField(max_length=140, default='0')
    bar = models.CharField(max_length=140, default='0')
    busser = models.CharField(max_length=140, default='0')
    tip = models.CharField(max_length=140, blank=True)
    total = models.CharField(max_length=140, default='0')

    def __str__(self):
        return str(self.id)

    def tip_is_positive(self):
        if float(tip) >= 0:
            return True
        else:
            return False
