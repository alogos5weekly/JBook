# Generated by Django 2.2.2 on 2019-07-14 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_post_is_anonymous'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=2),
        ),
    ]