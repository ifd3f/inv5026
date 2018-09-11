from django.db import models

# Create your models here.
import datetime
import functools
import json

from django.core import validators
from django.db import models
from django.db.models import Q


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    desc = models.TextField(default='')

    def serialized(self):
        return {
            'name': self.name,
            'id': self.id
        }

    def __str__(self):
        return self.name


class Box(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.ForeignKey(Location)
    desc = models.TextField(default='')
    mod_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.mod_date = datetime.datetime.now()
        super().save(*args, **kwargs)

    def serialized(self):
        return {
            'name': self.name,
            'id': self.id,
            'location': self.location.serialized()
        }

    def __str__(self):
        return '{} in {}'.format(self.name, self.location)

    class Meta:
        verbose_name_plural = 'boxes'


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0, validators=[validators.MinValueValidator(0)])
    box = models.ForeignKey(to=Box)
    # lt_alert = models.IntegerField(default=0, blank=True)
    tags = models.ManyToManyField(to=Tag, blank=True)
    desc = models.TextField(default='', blank=True)
    # mod_date = models.DateTimeField()
    shop_url = models.CharField(max_length=500, default='', blank=True)

    def save(self, *args, **kwargs):
        # self.mod_date = datetime.datetime.now()
        super().save()

    def render_tags(self):
        return ', '.join(map(lambda t: '<a href="/tag/{t.name}">{t.name}</a>'.format(t=t), self.tags.all()))

    def __str__(self):
        return '{} x {} in {} in {}'.format(self.name, self.quantity, self.box.name, self.box.location.name)

    def serialized(self):
        return {
            'name': self.name,
            'quantity': self.quantity,
            'box': self.box.serialized(),
            'desc': self.desc,
            'id': self.id,
            'tags': [t.name for t in self.tags.all()],
        }