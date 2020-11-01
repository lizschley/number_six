''' These are the models for almost all the functionality on this web-site.'''
import uuid
from django.core.exceptions import ValidationError
from django.db import models
from autoslug import AutoSlugField


class Category(models.Model):
    ''' one to many with groups '''
    BLOG = 'blog'
    RESUME = 'resume'
    FLASH_CARD = 'flash_card'
    EXERCISE = 'exercise'
    CATEGORY_TYPE_CHOICES = [
        (BLOG, 'Blog'),
        (RESUME, 'Resume'),
        (FLASH_CARD, 'Flash Card'),
        (EXERCISE, 'Exercise'),
    ]
    title = models.CharField(max_length=120, blank=False, unique=True)
    slug = AutoSlugField(max_length=150, unique=True, populate_from='title')
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES,
                                     default=FLASH_CARD)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return (f'<Category id: {self.id}, title: {self.title}, category_type: {self.category_type}, '
                f'slug: {self.slug}>')

    def __str__(self):
        return (f'<Category id: {self.id}, title: {self.title}, category_type: {self.category_type}, '
                f'slug: {self.slug}>')

    class Meta:
        get_latest_by = 'updated_at'


class Reference(models.Model):
    ''' Many to many with Paragraphs '''
    link_text = models.CharField(max_length=100, blank=False, unique=True)
    slug = AutoSlugField(max_length=150, blank=False, unique=True, populate_from='link_text')
    url = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'<Reference link_text: {self.link_text}>'

    def __str__(self):
        return f'<Reference link_text: {self.link_text}>'

    class Meta:
        verbose_name = 'reference'
        get_latest_by = 'updated_at'


class Paragraph(models.Model):
    ''' Many to many with References and with Groups '''
    subtitle = models.CharField(blank=True, max_length=120, db_index=True)
    note = models.TextField(blank=True)
    text = models.TextField(blank=True)
    standalone = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    references = models.ManyToManyField(Reference, through='ParagraphReference')
    image_path = models.CharField(max_length=100, blank=True)
    image_info_key = models.CharField(max_length=20, default='default')
    guid = models.CharField(max_length=36, editable=False, null=False, unique=True, default=uuid.uuid4)

    def clean(self):
        if self.standalone and not self.subtitle:
            raise ValidationError(f'guid=={self.guid}: subtitles for standalone paras are required.')
        if self.standalone and \
           Paragraph.objects.exclude(guid=self.guid).filter(subtitle__iexact=self.subtitle).exists():
            raise ValidationError(f'guid=={self.guid}: subtitles for standalone paras must be unique.')

    def __repr__(self):
        return (f'<Paragraph id: {self.id}, guid: {self.guid}, standalone: {self.standalone}'
                f', subtitle: {self.subtitle}>')

    def __str__(self):
        return (f'<Paragraph id: {self.id}, guid: {self.guid}, standalone: {self.standalone}'
                f', subtitle: {self.subtitle}>')

    class Meta:
        get_latest_by = 'updated_at'


class Group(models.Model):
    ''' Many to many with Paragraphs '''
    title = models.CharField(max_length=120, blank=False, unique=True)
    slug = AutoSlugField(max_length=150, unique=True, populate_from='title')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paragraphs = models.ManyToManyField(Paragraph, through='GroupParagraph')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    short_name = models.CharField(max_length=36, blank=False, unique=True, default=uuid.uuid4)
    cat_sort = models.PositiveSmallIntegerField(blank=True, null=True)

    def __repr__(self):
        return (f'<Group id: {self.id}, title: {self.title}, title_note: {self.note}, '
                f'category_id: {self.category_id}, slug: {self.slug}, short_name: {self.short_name}>')

    def __str__(self):
        return f'<Group id: {self.id}, title: {self.title}, short_name: {self.short_name}>'

    class Meta:
        get_latest_by = 'updated_at'


class GroupParagraph(models.Model):
    '''Association table where specialized order is set for paragraphs within a group'''
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'<Group id: {self.group}, para: {self.paragraph}, order: {self.order}>'

    def __str__(self):
        return f'<Group id: {self.group}, para: {self.paragraph}, order: {self.order}>'


class ParagraphReference(models.Model):
    '''Simple association table'''
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'<Reference id: {self.reference}, para: {self.paragraph}>'

    def __str__(self):
        return f'<Reference id: {self.reference}, para: {self.paragraph}>'
