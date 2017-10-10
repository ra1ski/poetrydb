# -*- coding: utf-8 -*-
from django.db import models
from django.http import Http404
from django.views import generic
from django.shortcuts import render
from .models import Poet, Poem, View, Theme, Age
from .helpers import get_slug_data_for_letter


class IndexView(generic.TemplateView):
    template_name = 'poetry/index.html'


class PoetDetailView(generic.DetailView):
    model = Poet


class PoetTopView(generic.DetailView):
    model = Poet
    template_name = 'poetry/poet_top.html'


class PoetAboutView(generic.DetailView):
    model = Poet
    template_name = 'poetry/poet_about.html'


class LetterDetailView(generic.View):
    template_name = 'poetry/poets-list-by-letter.html'

    def get(self, request, letter_id):
        slug_data = get_slug_data_for_letter()

        try:
            poets = Poet.objects.filter(letter=slug_data[letter_id.lower()], is_active=1).order_by('name')
        except Poet.ObjectDoesNotExist:
            raise Http404("Poll does not exist")

        return render(request, self.template_name, {'poets': poets, 'letter': letter_id})


class PoemDetailView(generic.DetailView):
    model = Poem
    template_name = 'poetry/poem-detail.html'

    def get(self, request, poet_id, slug_id, id):
        try:
            poem = Poem.objects.get(id=id, author_id=poet_id)

            if poem.is_shown == 0 and (not request.user or request.user.id != poem.added_user_id):
                raise Http404('Page not found')
        except Poem.DoesNotExist:
            raise Http404('Page not found')

        view, created = View.objects.get_or_create(poem_id=poem.id)
        view.views_count = view.views_count + 1
        view.save()
        poet = Poet.objects.get(id=poet_id)

        return render(request, self.template_name, {
            'poem': poem,
            'poet': poet,
        })


class ThemesView(generic.ListView):
    model = Theme

    def get_queryset(self):
        return (Theme.objects
                .values('id', 'name')
                .annotate(poems_count=models.Count(models.Case(models.When(poem__is_shown=1, then=1)))))


class ThemesDetailView(generic.DetailView):
    model = Theme
    template_name = 'poetry/theme_detail_list.html'

    def get_context_data(self, **kwargs):
        context = super(ThemesDetailView, self).get_context_data(**kwargs)
        context['poems'] = Poem.objects.filter(theme__id=self.get_object().id, is_shown=1)

        return context


class AgeDetailView(generic.DetailView):
    model = Age


class GenderListView(generic.ListView):
    model = Poet
    template_name = 'poetry/gender_list.html'
    gender_list = {
        'er-adam': {
            'id': 1,
            'label': 'Ер ақын',
        },
        'aiel-adam': {
            'id': 2,
            'label': 'Әйел ақын',
        },
    }

    def get(self, request, gender_id):
        gender = self.gender_list[gender_id]
        poets = (Poet.objects
                 .filter(sex=gender['id'])
                 .values('id', 'name', 'slug')
                 .annotate(models.Count("id"), poems_count=models.Count('poem__id'))
                 .order_by('name'))

        return render(request, self.template_name, {
            'gender': gender['label'],
            'poets': poets
        })


class PoemsTopView(generic.ListView):
    model = Poem
    template_name = 'poetry/poems/top.html'

    def get_queryset(self):
        return (Poem.objects
                .filter(is_shown=1)
                .values('id', 'title', 'author__id', 'author__name', 'author__slug', 'view__views_count')
                .order_by('-created_at')[:100])


class PoemsLastView(generic.ListView):
    model = Poem
    template_name = 'poetry/poems/last.html'

    def get_queryset(self):
        return (Poem.objects
                .filter(is_shown=1, author__is_active=1)
                .values('id', 'title', 'author__id', 'author__name', 'author__slug')
                .order_by('-created_at')[:100])
