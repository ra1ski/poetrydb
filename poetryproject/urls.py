from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from poetry.views import HomeView

urlpatterns = [
                  url(r'^$', HomeView.as_view(), name = 'home'),
                  url(r'^poetry/', include('poetry.urls')),
                  url(r'^user/', include('user.urls')),
                  url(r'^admin/', admin.site.urls),
                  url(r'^tinymce/', include('tinymce.urls')),
                  url(r'^page/', include('page.urls'))
              ] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
