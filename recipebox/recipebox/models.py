from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=40)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.username


class Recipe(models.Model):
    title = models.CharField(max_length=40)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    time_req = models.IntegerField()
    instructions = models.TextField()

    def __str__(self):
        return f"{self.title} -- by {self.author.user.username}"
