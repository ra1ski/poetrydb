from django.contrib.auth import views as authviews
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views as userviews

app_name = 'user'
urlpatterns = [
    # auth
    url(r'^signup/', userviews.SignUpView.as_view(), name='user_signup'),
    url(r'^login/$', userviews.LoginView.as_view(), name='user_login'),
    url(r'^logout/$', authviews.logout, {'next_page': 'user:user_login'}, name='user_logout'),
    url(r'^activate/(?P<id>[0-9]+)/(?P<hash>[a-z0-9]{32})/$', userviews.ActivateView.as_view(), name='user_activate'),

    # cabinet
    url(r'^(?P<pk>[0-9]+)/$', userviews.IndexView.as_view(), name='user_home'),
    url(r'^(?P<pk>[0-9]+)/all/$', userviews.AllPoemsView.as_view(), name='user_all_poems'),
    url(r'^offer-poem/$', login_required(userviews.OfferPoem.as_view()), name='offer_poem'),
    url(r'^(?P<pk>[0-9]+)/edit/$', login_required(userviews.EditUserView.as_view()), name='edit_profile'),
    url(r'^contributors/$', userviews.TopContributors.as_view(), name='user_top_contributors'),
]
