# Generated by Django 3.2.7 on 2022-05-02 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_auto_20220502_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='serie',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='serie',
        ),
        migrations.DeleteModel(
            name='Serie',
        ),
    ]
