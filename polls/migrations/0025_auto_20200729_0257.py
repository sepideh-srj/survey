# Generated by Django 3.0.3 on 2020-07-29 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0024_auto_20200729_0245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionforuser',
            name='ambientPic',
        ),
        migrations.RemoveField(
            model_name='questionforuser',
            name='flashPic',
        ),
    ]
