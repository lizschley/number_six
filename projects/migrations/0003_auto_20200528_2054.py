# Generated by Django 3.0.6 on 2020-05-28 20:54

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'get_latest_by': 'updated_at',
            },
        ),
        migrations.CreateModel(
            name='GroupParagraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtitle', models.CharField(blank=True, db_index=True, max_length=120)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, max_length=150, populate_from='subtitle')),
                ('note', models.TextField(blank=True)),
                ('text', models.TextField(blank=True)),
                ('standalone', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(through='projects.GroupParagraph', to='projects.Group')),
            ],
            options={
                'get_latest_by': 'updated_at',
            },
        ),
        migrations.RemoveField(
            model_name='project',
            name='technology',
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_text', models.CharField(max_length=100, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='link_text', unique=True)),
                ('url', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('paragraphs', models.ManyToManyField(to='projects.Paragraph')),
            ],
            options={
                'verbose_name': 'reference',
                'get_latest_by': 'updated_at',
            },
        ),
        migrations.AddField(
            model_name='groupparagraph',
            name='paragraph',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Paragraph'),
        ),
    ]