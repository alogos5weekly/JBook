# Generated by Django 2.2.2 on 2019-12-24 06:12

from django.db import migrations, models
import studymaterial.models


class Migration(migrations.Migration):

    dependencies = [
        ('studymaterial', '0003_auto_20191224_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(null=True, upload_to=studymaterial.models.get_upload_path),
        ),
    ]