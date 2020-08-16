import uuid
from django.db import migrations


def populate_reference(apps, schema_editor):
    Paragraph = apps.get_model('projects', 'Paragraph')
    for obj in Paragraph.objects.all():
        obj.guid = uuid.uuid4()
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_paragraph_guid'),
    ]

    operations = [
        migrations.RunPython(populate_reference),
    ]