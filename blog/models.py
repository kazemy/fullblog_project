from django.db import models
from django.utils import timezone
#User table/model is created by django... so we import and will use it
#in the author field
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

    # using reverse to get the post instance abolute url
    def get_absolute_url(self):
        #first argument is the template name
        #second is the instance of a specific post primary key
        return reverse('post-detail', kwargs={'pk':self.pk})