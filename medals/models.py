from django.db import models
from django.contrib.auth.models import User

class Medals(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    year = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    person = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
