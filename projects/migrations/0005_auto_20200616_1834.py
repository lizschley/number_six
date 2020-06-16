# Generated by Django 3.0.7 on 2020-06-16 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_remove_paragraph_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paragraph',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='paragraphs',
        ),
        migrations.AddField(
            model_name='group',
            name='paragraphs',
            field=models.ManyToManyField(through='projects.GroupParagraph', to='projects.Paragraph'),
        ),
        migrations.CreateModel(
            name='ParagraphReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('paragraph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Paragraph')),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Reference')),
            ],
        ),
        migrations.AddField(
            model_name='paragraph',
            name='references',
            field=models.ManyToManyField(through='projects.ParagraphReference', to='projects.Reference'),
        ),
    ]
