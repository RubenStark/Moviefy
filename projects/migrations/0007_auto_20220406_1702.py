# Generated by Django 3.2.7 on 2022-04-06 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20220406_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectViews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='movie_views',
            field=models.IntegerField(default=1),
        ),
    ]
