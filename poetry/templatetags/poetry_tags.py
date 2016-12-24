from django import template
from poetry.models import Age, Poem, Poet

register = template.Library()


@register.inclusion_tag('poetry/blocks/_age_menu.html')
def age_menu():
    ages = Age.objects.all()

    return {'ages': ages}


@register.inclusion_tag('poetry/blocks/_last_added.html')
def last_added_poems():
    poems = Poet.objects.raw('''
		SELECT
			poem.id, poem.title, poet.id as poet_id, poet.slug, poet.name as poet_name
		FROM
			poetry_poem as poem
		LEFT JOIN poetry_poet as poet ON poet.id=poem.author_id
		WHERE poet.is_active=1 AND poem.is_shown=1
		ORDER BY poem.created_at DESC
		LIMIT 10
	''')

    return {'poems': poems}


@register.inclusion_tag('poetry/blocks/_top_poems.html')
def top_poems():
    poems = Poem.objects.raw('''
			SELECT 
				poem.id, poem.title, views.views_count, poet.name, poet.slug, poet.id as poet_id
			FROM 
				poetry_poem as poem
			LEFT JOIN poetry_view as views ON poem.id=views.poem_id
			LEFT JOIN poetry_poet as poet ON poet.id=poem.author_id
			WHERE poet.is_active=1 AND poem.is_shown=1
			ORDER BY views.views_count DESC
			LIMIT 10
		''')

    return {'poems': poems}


@register.inclusion_tag('poetry/blocks/_poets_list.html')
def poets_list_alphabetical(column_nb):
    # poets = Poet.objects.filter(is_active=1)
    poets = Poet.objects.raw('''
		SELECT 
			poet.id, poet.name, poet.slug, COUNT(poem.id) as poems_count
		FROM 
			poetry_poet as poet
		LEFT JOIN poetry_poem as poem ON poet.id=poem.author_id AND poem.is_shown=1
		WHERE poet.is_active=1
		GROUP BY poet.id
		ORDER BY poet.name
	''')

    return {'poets': poets, 'column_nb': column_nb}


@register.inclusion_tag('poetry/blocks/_user_poems_list.html')
def get_user_poems_list(user, user_id, limit):
    poems = Poem.objects.raw('''
		SELECT 
			poem.id, poem.title, poet.name, poet.slug, poet.id as poet_id, poem.is_shown
		FROM 
			poetry_poem as poem
		LEFT JOIN poetry_poet as poet ON poet.id=poem.author_id
		WHERE poem.added_user_id=%s
		ORDER BY poem.created_at DESC
		LIMIT %s
	''', [user_id, limit])

    return {'user': user, 'poems': poems, 'user_id': user_id}


@register.inclusion_tag('poetry/blocks/_social_buttons.html')
def social_buttons():
    pass
