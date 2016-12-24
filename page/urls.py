from django.conf.urls import url
from . import views

app_name = 'page'
urlpatterns = [
    url(r'^(?P<slug>[a-z-]+)/$', views.ShowView.as_view(), name = 'show'),
]
