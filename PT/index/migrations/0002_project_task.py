# Generated by Django 2.1.4 on 2019-07-20 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('category', models.IntegerField(choices=[(0, '功能测试'), (1, '自动化测试'), (2, '性能测试')], default=0)),
                ('status', models.IntegerField(choices=[(0, '需求确认'), (1, '测试准备'), (2, '测试进行'), (3, '测试收尾'), (4, '等待上线'), (5, '结束归档')], default=0)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Users')),
            ],
        ),
    ]
