# Generated by Django 3.0.3 on 2020-06-30 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_user_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='code',
            field=models.IntegerField(default=0),
        ),
    ]
