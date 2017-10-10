from django import template
from django.db import models
from poetry.models import Age, Poem, Poet

register = template.Library()


@register.inclusion_tag('poetry/blocks/_age_menu.html')
def age_menu():
    ages = Age.objects.all()

    return {'ages': ages}


@register.inclusion_tag('poetry/blocks/_last_added.html')
def last_added_poems():
    poems = (Poem.objects
             .filter(is_shown=1, author__is_active=1)
             .values('id', 'title', 'author__id', 'author__slug', 'author__name')
             .order_by('-created_at')[:10])

    return {'poems': poems}


@register.inclusion_tag('poetry/blocks/_top_poems.html')
def top_poems():
    poems = (Poem.objects
             .filter(is_shown=1, author__is_active=1)
             .values('id', 'title', 'author__id', 'author__slug', 'author__name', 'view__views_count')
             .order_by('-view__views_count')[:10])

    return {'poems': poems}


@register.inclusion_tag('poetry/blocks/_poets_list.html')
def poets_list_alphabetical(column_nb):
    poets = (Poet.objects
             .filter(is_active=1)
             .values('id', 'name', 'slug')
             .annotate(poems_count=models.Count(models.Case(models.When(poem__is_shown=1, then=1)))))

    return {'poets': poets, 'column_nb': column_nb}


@register.inclusion_tag('poetry/blocks/_user_poems_list.html')
def get_user_poems_list(user, user_id, limit):
    poems = (Poem.objects
             .filter(added_user=1)
             .values('id', 'title', 'author__name', 'author__slug', 'author__id', 'is_shown')
             .order_by('-created_at'))[:limit]

    return {'user': user, 'poems': poems, 'user_id': user_id}


@register.inclusion_tag('poetry/blocks/_social_buttons.html')
def social_buttons():
    pass
