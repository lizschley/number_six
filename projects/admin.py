from django.contrib import admin
from projects.models.projects import Project
from projects.models.paragraphs import Paragraph
from projects.models.paragraphs import Group
from projects.models.paragraphs import Reference
from projects.models.paragraphs import GroupParagraph

# Register your models here.
admin.site.register(Project)
admin.site.register(Paragraph)
admin.site.register(Group)
admin.site.register(Reference)
admin.site.register(GroupParagraph)
