# Generated by Django 2.2.2 on 2019-06-08 16:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, upload_to='')),
                ('about', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, max_length=250)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('branch', models.CharField(choices=[('CS', 'Computer Science & Engineering'), ('ME', 'Mechanical Engineering'), ('EE', 'Electrical Engineering'), ('ECE', 'Electornics & Communication Engineering'), ('CE', 'Civil Engineering'), ('IT', 'Information Technology')], max_length=3)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
