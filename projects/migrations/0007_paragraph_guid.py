# Generated by Django 3.0.7 on 2020-08-11 18:33
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20200804_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='paragraph',
            name='guid',
            field=models.UUIDField(null=True),
        ),
    ]