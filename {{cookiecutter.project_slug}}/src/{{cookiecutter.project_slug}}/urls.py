# -*- coding: utf-8 -*-

"""{{cookiecutter.project_slug}} URL Configuration

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
from django.conf.urls import url, include
# from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

import xadmin
xadmin.autodiscover()

from xadmin.plugins import xversion
xversion.register_models()

from django.conf.urls import handler404, handler500

from {{cookiecutter.project_slug}}.base import views as base_views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'xadmin/', include(xadmin.site.urls)),
    url(r'^$', base_views.home, name='home'),
    url(r'admin/', include(xadmin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

handler404 = base_views.error_404
handler500 = base_views.error_500
