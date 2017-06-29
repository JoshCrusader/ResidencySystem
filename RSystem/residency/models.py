from django.db import models
from django.contrib.auth.models import User
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=100, primary_key= True)
    def __str__(self):
        return 'Author: {} {}'.format(self.last_name,self.first_name)


class Team(models.Model):
    name = models.CharField(max_length=100)
class Project(models.Model):
    name = models.CharField(max_length=100)
    stat = models.CharField(max_length=100)
    specs = models.TextField()
    team = models.ForeignKey(Team, null = True)
class Acc(models.Model):
    user = models.OneToOneField(User)
    team = models.ForeignKey(Team, null = True)
    valid = models.BooleanField(default = False)

class Objective(models.Model):
    name = models.CharField(max_length=100)
    points = models.IntegerField()
    done = models.BooleanField(default = False)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)

class Status(models.Model):
    value = models.CharField(max_length = 2000)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)