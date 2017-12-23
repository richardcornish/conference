from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path

from .views import FaviconView, HomeView, RobotsView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('about.urls')),
    path('search/', include('search.urls')),
    path('text/', include('sms.urls')),
    path('call/', include('voice.urls')),
    path('favicon.ico', FaviconView.as_view(), name='favicon'),
    path('robots.txt', RobotsView.as_view(), name='robots'),
    path('', include('sitemaps.urls')),
    path('', HomeView.as_view(), name='home'),
]


# Static/media for local development
if getattr(settings, 'DEBUG', False):
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [re_path(r'^__debug__/', include('debug_toolbar.toolbar'))]
