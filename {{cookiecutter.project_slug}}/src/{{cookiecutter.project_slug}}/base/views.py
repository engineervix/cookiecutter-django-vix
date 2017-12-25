#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
views.
"""

from __future__ import absolute_import, unicode_literals

from django.shortcuts import render

__author__ = "{{ cookiecutter.author_name }}"
__copyright__ = "Copyright {% now 'utc', '%Y' %}, {{ cookiecutter.author_name }}"
# __credits__ = []
__license__ = ""
__version__ = '{{ cookiecutter.version }}'
__maintainer__ = "{{ cookiecutter.author_name }}"
__email__ = "{{ cookiecutter.email }}"
__status__ = "Production"


def home(request):
        data = {}
        return render(request, 'base/base.html', data)


def error_404(request):
        data = {}
        return render(request, 'error_404.html', data)


def error_500(request):
        data = {}
        return render(request, 'error_500.html', data)
