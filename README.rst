###################
Django tabbed admin
###################

Simple library to easilly add tabs to admin forms. It also allows users to re-order inlines and fieldsets.
Django tabbed admin is compatible with django-grappelli and django-gipsy.

*******
Install
*******

It is strongly recommanded to install this theme from GIT with PIP onto you project virtualenv.

From Github

.. code-block::  shell-session

    https://github.com/omji/django-tabbed-admin#egg=tabbed_admin


*****
setup
*****

Simply add the app in your installed apps list in settings.py

.. code-block::  python

    INSTALLED_APPS = (
        ...
        'tabbed_admin'
        ...
    )

Django-tabbed-admin by default requires Jquery UI tabs plugin in order to work. It is packaged with the static files required to make it funcitonnal, however, they are not activated by default to avoid a conflict with other libraries.

In order to activate the Jquery UI statics, add the following line to the project settings:

.. code-block::  python

    TABBED_ADMIN_USE_JQUERY_UI = True


********************
Configure admin tabs
********************

In order to add tabs to a model admin, it should inherit from tabbed_admin.TabbedModelAdmin and contain a tabs attribute.
The tab attribute configuration tries to remain similar to the fieldsets and inlines setup logic.

.. code-block::  python

    from django.contrib import admin

    from tabbed_admin import TabbedModelAdmin
    from .models import Band, Musician, Album


    class MusicianInline(admin.StackedInline):
        model = Musician
        extra = 1


    class AlbumInline(admin.TabularInline):
        model = Album
        extra = 1


    @admin.register(Band)
    class BandAdmin(TabbedModelAdmin):
        model = Band

        tab_overview = (
            (None, {
                'fields': ('name', 'bio', 'style')
            }),
            MusicianInline,
            ('Contact', {
                'fields': ('agent', 'phone', 'email')
            })
        )
        tab_album = (
            AlbumInline,
        )
        tabs = [
            ('Overview', tab_overview),
            ('Albums', tab_album)
        ]

Be warned that the tabs will completely reset the fieldsets and inlines attributes in order to avoid conflicts during the form saving. Both attributes are overwritten with the entries passed to the tabs attribute. For the same reasons, it is highly recommanded not to overwrite get_fieldsets or get_inlines.

You can pass and modify the tabs dynamically the same way you would do for fieldsets or inlines.

.. code-block::  python

    class BandAdmin(TabbedModelAdmin):
        model = Band

        tab_overview = (
            (None, {
                'fields': ('name', 'bio', 'style')
            }),
            MusicianInline,
            ('Contact', {
                'fields': ('agent', 'phone', 'email')
            }),
        )
        tab_ressources = (
            ConcertInline,
            AlbumInline,
        )
        tabs = [
            ('Overview', tab_overview),
            ('Ressources', tab_ressources)
        ]

        def get_tabs(self, request, obj=None):
            tabs = self.tabs
            if obj is not None:
                tab_overview = self.tab_overview + ('Social', {
                    'fields': ('website', 'twitter', 'facebook')
                })
                tab_ressources = self.tab_ressources + (InterviewInline, )
                tabs = [
                    ('Overview', tab_overview),
                    ('Ressources', tab_ressources)
                ]
            self.tabs = tabs
            return super(BandAdmin, self).get_tabs(request, obj)


************
Contribution
************

Please feel free to contribute. Any help and advices are much appreciated.
You will find an exemple application to run and develop the library easily.


*****
LINKS
*****

Development:
    https://github.com/omji/django-tabbed-admin
