# Generated by Django 3.2.7 on 2022-04-22 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_project_progress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='progress',
        ),
        migrations.AddField(
            model_name='watched',
            name='progress',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
