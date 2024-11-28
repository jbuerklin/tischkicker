"""
URL configuration for tischkicker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
import re
from urllib.parse import urlsplit

from django.core.exceptions import ImproperlyConfigured
from django.urls import re_path
from django.views.static import serve


def static_for_debug_false(prefix, view=serve, **kwargs):
    """
    the same as django.conf.urls.static.static, but works when debug is false
    """
    if not prefix:
        raise ImproperlyConfigured("Empty static prefix not permitted")
    elif urlsplit(prefix).netloc:
        # No-op if a non-local prefix.
        return []
    return [
        re_path(
            r"^%s(?P<path>.*)$" % re.escape(prefix.lstrip("/")), view, kwargs=kwargs
        ),
    ]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('braschüne.urls')),
    path('accounts/', include('allauth.urls')),
] + static_for_debug_false(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static_for_debug_false(settings.STATIC_URL, document_root=settings.STATIC_ROOT)