# Generated by Django 3.0.3 on 2020-07-17 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_auto_20200716_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='experience',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(default='', max_length=10),
        ),
    ]
