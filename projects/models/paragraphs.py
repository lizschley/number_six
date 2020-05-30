from django.db import models
from autoslug import AutoSlugField


class Group(models.Model):
    title = models.CharField(max_length=120, blank=False, unique=True)
    slug = AutoSlugField(unique=True, populate_from='title')
    note = models.TextField(blank=True)

    def __repr__(self):
        return f'<Group id: {self.id}, title: {self.title}>'

    class Meta:
        get_latest_by = 'updated_at'


class Paragraph(models.Model):
    subtitle = models.CharField(blank=True, max_length=120, db_index=True)
    slug = AutoSlugField(populate_from='subtitle', max_length=150, db_index=True)
    note = models.TextField(blank=True)
    text = models.TextField(blank=True)
    standalone = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(Group, through='GroupParagraph')

    # TODO display first 20 characters of text field
    def __repr__(self):
        return f'<Paragraph {self.subtitle}>'

    class Meta:
        get_latest_by = 'updated_at'


class GroupParagraph(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reference(models.Model):
    link_text = models.CharField(max_length=100, blank=False, unique=True)
    slug = AutoSlugField(blank=False, unique=True, populate_from='link_text')
    url = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paragraphs = models.ManyToManyField(Paragraph)

    def __repr__(self):
        return f'<Reference {self.link_text}>'

    class Meta:
        verbose_name = 'reference'
        get_latest_by = 'updated_at'

