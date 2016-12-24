from . import views
from django.conf.urls import url

app_name = 'poetry'
urlpatterns = [
    url(r'^authors/$', views.IndexView.as_view(), name = 'authors'),
    url(r'^authors/(?P<pk>[0-9]+)-(?P<slug_id>[a-z-]+)/$', views.PoetDetailView.as_view(), name = 'poet'),
    url(r'^authors/(?P<pk>[0-9]+)-(?P<slug_id>[a-z-]+)/top/$', views.PoetTopView.as_view(), name = 'poet_top'),
    url(r'^authors/(?P<pk>[0-9]+)-(?P<slug_id>[a-z-]+)/about/$', views.PoetAboutView.as_view(), name = 'poet_about'),
    url(r'^authors/(?P<letter_id>[А-ЯӘІҢҒҮҰҚӨҺ]+)/$', views.LetterDetailView.as_view(), name = 'letter'),
    url(r'^authors/(?P<poet_id>[0-9]+)-(?P<slug_id>[a-z-]+)/(?P<id>[0-9]+)/$', views.PoemDetailView.as_view(),
        name = 'poem'),

    url(r'^themes/$', views.ThemesView.as_view(), name = 'themes'),
    url(r'^themes/(?P<pk>[0-9]+)/$', views.ThemesDetailView.as_view(), name = 'themes_detail'),

    url(r'^poems/top100/$', views.PoemsTopView.as_view(), name = 'poems_top_100'),
    url(r'^poems/$', views.PoemsLastView.as_view(), name = 'poems_last'),

    url(r'^age/(?P<pk>[0-9]+)/$', views.AgeDetailView.as_view(), name = 'age_detail'),
    url(r'^authors/(?P<gender_id>[a-z-]+)/$', views.GenderListView.as_view(), name = 'gender_list'),
]
