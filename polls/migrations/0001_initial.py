# Generated by Django 3.0.3 on 2020-04-14 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.IntegerField(default=0)),
                ('flashPic', models.ImageField(upload_to='images/')),
                ('ambientPic', models.ImageField(upload_to='images/')),
                ('blendedPic', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.IntegerField(default=0)),
                ('pointer', models.IntegerField(blank=True, default=0)),
                ('order', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flash', models.IntegerField(default=0)),
                ('ambient', models.IntegerField(default=0)),
                ('flashTemp', models.IntegerField(default=0)),
                ('ambientTemp', models.IntegerField(default=0)),
                ('ambientBrightness', models.FloatField(default=0)),
                ('user', models.IntegerField(default=0)),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Question')),
            ],
        ),
    ]
