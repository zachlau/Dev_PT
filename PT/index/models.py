from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=10, unique=True, null=False)
    password = models.CharField(max_length=10, null=False)
    sex = models.IntegerField(default=2)
    email = models.EmailField(null=False, unique=True)

class Project(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False)

class Task(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category = models.IntegerField(choices=((0, '功能测试'), (1, '自动化测试'), (2, '性能测试')), default=0)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    status = models.IntegerField(choices=((0, '需求确认'), (1, '测试准备'), (2, '测试进行'), (3, '测试收尾'), (4, '等待上线'), (5, '结束归档')), default=0)
    avalible = models.IntegerField(choices=((0, '无效'), (1, '有效')), default=1)

class Cases(models.Model):
    number = models.CharField(max_length=20, unique=True, null=False)
    desc = models.CharField(max_length=50, null=False)
    url = models.URLField(null=False)
    method = models.CharField(max_length=10, null=False)
    headers = models.TextField(null=True)
    type = models.CharField(max_length=10, null=True)
    body = models.TextField(null=True)
    checks = models.CharField(max_length=200, null=False)