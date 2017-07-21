# coding: utf-8

# DJANGO IMPORTS
from django.conf import settings

# Activate the library jquery ui
USE_JQUERY_UI = getattr(settings, "TABBED_ADMIN_USE_JQUERY_UI", False)
USE_GRAPPELLI = getattr(settings, "TABBED_ADMIN_USE_GRAPPELLI", False)

# Default jquery ui css and js
DEFAULT_JQUERY_UI_CSS = 'tabbed_admin/css/jquery-ui-1.11.4.min.css'
DEFAULT_JQUERY_UI_JS = 'tabbed_admin/js/jquery-ui-1.11.4.min.js'

# User ability to override the default css and js
JQUERY_UI_CSS = getattr(
    settings, "TABBED_ADMIN_JQUERY_UI_CSS", DEFAULT_JQUERY_UI_CSS)
JQUERY_UI_JS = getattr(
    settings, "TABBED_ADMIN_JQUERY_UI_JS", DEFAULT_JQUERY_UI_JS)
