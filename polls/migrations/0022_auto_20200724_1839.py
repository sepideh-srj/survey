# Generated by Django 3.0.3 on 2020-07-25 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0021_user_numberofpics'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='flash',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='temp',
            field=models.IntegerField(default=0),
        ),
    ]
