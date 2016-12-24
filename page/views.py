# -*- coding: utf-8 -*-
from django.views import generic
from .models import Page


class ShowView(generic.DetailView):
    model = Page
