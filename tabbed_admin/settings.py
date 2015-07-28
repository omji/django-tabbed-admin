# coding: utf-8

# DJANGO IMPORTS
from django.conf import settings

# Activate the library jquery ui
USE_JQUERY_UI = getattr(settings, "TABBED_ADMIN_USE_JQUERY_UI", False)
