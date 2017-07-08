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
    cubes = models.CharField(max_length = 20, default = "LEXELL")
class Project(models.Model):
    name = models.CharField(max_length=100)
    stat = models.CharField(max_length=100)
    specs = models.TextField()
    team = models.ForeignKey(Team, null = True)
    def __str__(self):
        return "Project: {}".format(self.name)
class Acc(models.Model):
    user = models.OneToOneField(User)
    team = models.ForeignKey(Team, null = True)
    valid = models.BooleanField(default = False)
    def __str__(self):
        return "Acc: {}".format(self.user.first_name)
class Objective(models.Model):
    name = models.CharField(max_length=100)
    points = models.IntegerField()
    done = models.BooleanField(default = False)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)

class Status(models.Model):
    value = models.CharField(max_length = 45)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)

class Progress(models.Model):
    value = models.CharField(max_length = 2000)
    cdate = models.DateTimeField(editable=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)

class Role(models.Model):
    acc = models.ForeignKey(Acc, on_delete = models.CASCADE)
    proj = models.ForeignKey(Project, on_delete = models.CASCADE)
    content = models.CharField(max_length = 45)


class teamSched(models.Model):
    team = models.ForeignKey(Team, on_delete = models.CASCADE)
    day = models.IntegerField()
    start = models.CharField(max_length = 5)
    end = models.CharField(max_length = 5)

class resident(models.Model):
    acc = models.ForeignKey(Acc, on_delete=models.CASCADE)
    cdate = models.DateTimeField(editable=False)
    edate = models.DateTimeField(editable=False, null = True)