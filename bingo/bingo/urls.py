"""bingo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from .admin import bingo_admin_site

urlpatterns = [
    url(r'^admin/', bingo_admin_site.urls),

    url(r'api/', include('api.urls')),

    url(r'api-auth/',
        include(('rest_auth.urls', 'rest_auth'), namespace='rest_auth')),

    url(r'api-registration/',
        include(('rest_auth.registration.urls', 'rest_auth.registration'),
                namespace='rest_registration')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
