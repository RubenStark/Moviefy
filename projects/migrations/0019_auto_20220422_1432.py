# Generated by Django 3.2.7 on 2022-04-22 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_auto_20220421_1913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='progress',
        ),
        migrations.AddField(
            model_name='watchedepisode',
            name='progress',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
