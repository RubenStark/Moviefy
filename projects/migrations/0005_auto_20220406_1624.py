# Generated by Django 3.2.7 on 2022-04-06 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20220406_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='movie_views',
        ),
        migrations.AddField(
            model_name='project',
            name='movie_views',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.projectviews'),
        ),
    ]
