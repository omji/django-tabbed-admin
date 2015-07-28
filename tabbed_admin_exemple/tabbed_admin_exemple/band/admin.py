from django.contrib import admin

from tabbed_admin import TabbedModelAdmin
from .models import Band, Musician, Concert, Album, Interview


class MusicianInline(admin.StackedInline):
    model = Musician
    extra = 1


class ConcertInline(admin.TabularInline):
    model = Concert
    extra = 1


class AlbumInline(admin.TabularInline):
    model = Album
    extra = 1


class InterviewInline(admin.TabularInline):
    model = Interview
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
        }),
        ('Social', {
            'fields': ('website', 'twitter', 'facebook')
        })
    )
    tab_ressources = (
        ConcertInline,
        AlbumInline,
        InterviewInline
    )
    tabs = [
        ('Overview', tab_overview),
        ('Ressources', tab_ressources)
    ]
