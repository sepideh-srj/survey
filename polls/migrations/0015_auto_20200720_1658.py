# Generated by Django 3.0.3 on 2020-07-20 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_auto_20200708_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='firstTime',
            field=models.IntegerField(default=0),
        ),
    ]
