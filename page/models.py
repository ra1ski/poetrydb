# -*- coding: utf-8 -*-
from django.db import models
from tinymce.models import HTMLField


class Page(models.Model):
    title = models.CharField(max_length=255)
    content = HTMLField()
    slug = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
