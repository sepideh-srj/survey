# Generated by Django 3.0.3 on 2020-06-03 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20200603_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='ambientBrightness',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='choice',
            name='flashBrightness',
            field=models.FloatField(default=0),
        ),
    ]
