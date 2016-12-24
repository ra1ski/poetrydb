# -*- coding: utf-8 -*-
from .helpers import get_slug_data_for_letter, make_slug
from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField


class Age(models.Model):
    name = models.CharField(max_length = 255)
    description = HTMLField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def poets_with_count(self):
        return Poet.objects.raw('''
            SELECT
                poet.id, poet.name, poet.slug, COUNT(poem.id) as poems_count
            FROM 
                poetry_poet as poet
            LEFT JOIN poetry_poem as poem ON poet.id=poem.author_id AND poem.is_shown=1
            WHERE poet.age_id=%s
            GROUP BY poet.id
        ''', [self.id])


class Theme(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Poet(models.Model):
    name = models.CharField(max_length = 255)
    letter = models.CharField(max_length = 5)
    slug = models.SlugField(max_length = 255, unique = True)
    about = HTMLField(blank = True)
    age = models.ForeignKey(Age, blank = True, null = True)
    sex = models.SmallIntegerField(
        default = 1,
        choices = (
            (1, 'Ер адам'),
            (2, 'Әйел адам'),
        )
    )
    is_active = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def poems(self):
        return Poem.objects.filter(author_id = self.id, is_shown = 1)

    def poems_top(self):
        return Poem.objects.raw('''
            SELECT 
                poem.id, poem.title, views.views_count
            FROM 
                poetry_poem as poem
            LEFT JOIN poetry_view as views on views.poem_id=poem.id
            WHERE poem.author_id=%s AND poem.is_shown=1
            ORDER BY views.views_count DESC
        ''', [self.id])

    def save(self, *args, **kwargs):
        letters = get_slug_data_for_letter()
        letter = self.name.strip().lower()[0:1]
        self.letter = letters[letter]
        self.slug = make_slug(self.name)
        super(Poet, self).save(*args, **kwargs)


class Poem(models.Model):
    author = models.ForeignKey(Poet)
    title = models.CharField(max_length = 100)
    content = models.TextField()
    theme = models.ManyToManyField(Theme, blank = True, null = True)
    added_user = models.ForeignKey(User)
    is_shown = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    def views_count(self):
        return self.view_set.get(poem_id = self.id).views_count

    def poem_poet(self):
        return Poet.objects.get(pk = self.author_id)

    class Meta:
        ordering = ['title']


class View(models.Model):
    poem = models.ForeignKey(Poem)
    views_count = models.IntegerField(default = 0)
