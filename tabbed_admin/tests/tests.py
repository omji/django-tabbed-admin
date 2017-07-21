from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.template import Context
from django.test import TestCase
from django.test.client import RequestFactory, Client
from django.test.utils import override_settings

from tabbed_admin.settings import USE_JQUERY_UI
from tabbed_admin.templatetags.tabbed_admin_tags import render_tab_fieldsets_inlines
from tabbed_admin.tests.admin import BandAdmin, InterviewInline
from tabbed_admin.tests.models import Band


class MockRequest(object):
    pass


class MockSuperUser(object):
    is_active = True
    is_staff = True
    def has_perm(self, perm):
        return True

request = RequestFactory()
request.user = MockSuperUser()
request.csrf_processing_done = True


class TabbedModelAdminTest(TestCase):

    def setUp(self):
        self.site = AdminSite()

    def test_fieldsets_inline_attribute_populated(self):
        """
        Tests if self.inlines and self.fieldsets are correcly populated from
        the self.tabs attribute.
        """
        admin = BandAdmin(Band, self.site)
        self.assertIsNone(admin.fieldsets)
        self.assertEqual(0, len(admin.inlines))
        fieldsets = admin.get_fieldsets(request)
        inlines = admin.get_inline_instances(request)
        self.assertNotEqual(0, len(fieldsets))
        self.assertNotEqual(0, len(inlines))
        self.assertNotEqual(0, len(admin.fieldsets))
        self.assertNotEqual(0, len(admin.inlines))

    def test_fieldsets_inlines_overriden_by_tabs(self):
        """
        Tests if when set by default, fieldsets and inlines are properly
        overriden.
        """
        class TestBandAdmin(BandAdmin):
            fieldsets = (
                ('Social', {
                    'fields': ('website', 'twitter', 'facebook')
                })
            )
            inlines = (
                InterviewInline,
            )
        admin = TestBandAdmin(Band, self.site)
        self.assertEqual(admin.get_fieldsets(request),
                         admin.formatted_tabs['fieldsets'])
        inlines = admin.get_inline_instances(request)
        inlines = admin.inlines
        for inline in inlines:
            self.assertIn(inline, admin.formatted_tabs['inlines'])

    def test_get_tabs_overrides_tabs_attribute(self):
        """
        Tests if get_tabs method successfully overrides the self.tabs and returns it.
        """
        single_tab = [('Overview', BandAdmin.tab_overview)]
        class TestBandAdmin(BandAdmin):
            def get_tabs(self, request, obj=None):
                """
                Returns the tabs attribute.
                """
                tabs = self.tabs
                if obj is not None and obj.style == Band.STYLE_OVERRIDE:
                    tabs = single_tab
                self.tabs = tabs
                return super(TestBandAdmin, self).get_tabs(request, obj)

        admin = TestBandAdmin(Band, self.site)
        band = Band.objects.create(name="Test band", style=Band.STYLE_JAZZ)
        tabs = admin.get_tabs(request, band)
        self.assertEqual(len(tabs), 2)
        self.assertNotEqual(tabs, single_tab)
        band.style = Band.STYLE_OVERRIDE
        tabs = admin.get_tabs(request, band)
        self.assertEqual(len(tabs), 1)
        self.assertEqual(tabs, single_tab)

    def test_dynamically_add_fieldsets_inlines_to_tabs(self):
        """
        Tests overriding dynamically tabs via get_tabs.
        """
        added_fieldset = ('Social', {
            'fields': ('website', 'twitter', 'facebook')
        })
        added_inline = InterviewInline

        class TestBandAdmin(BandAdmin):
            def get_tabs(self, request, obj=None):
                tabs = self.tabs
                tab_overview = self.tab_overview + (added_fieldset, )
                tab_ressources = self.tab_ressources + (added_inline, )
                tabs = [
                    ('Overview', tab_overview),
                    ('Ressources', tab_ressources)
                ]
                self.tabs = tabs
                return super(TestBandAdmin, self).get_tabs(request, obj)

        original_admin = BandAdmin(Band, self.site)
        self.assertNotIn(added_fieldset, original_admin.get_fieldsets(request))
        self.assertNotIn(added_inline, original_admin.tab_ressources)
        admin = TestBandAdmin(Band, self.site)
        inlines_classes = []
        inlines = admin.get_inline_instances(request)
        for inline in inlines:
            inlines_classes.append(inline.__class__)
        self.assertIn(added_inline, inlines_classes)

    def test_version_previous_to_django(self):
        """
        Tests overriding dynamically tabs via get_tabs.
        """
        added_fieldset = ('Social', {
            'fields': ('website', 'twitter', 'facebook')
        })
        added_inline = InterviewInline

        class TestBandAdmin(BandAdmin):
            def get_tabs(self, request, obj=None):
                tabs = self.tabs
                tab_overview = self.tab_overview + (added_fieldset, )
                tab_ressources = self.tab_ressources + (added_inline, )
                tabs = [
                    ('Overview', tab_overview),
                    ('Ressources', tab_ressources)
                ]
                self.tabs = tabs
                return super(TestBandAdmin, self).get_tabs(request, obj)

        original_admin = BandAdmin(Band, self.site)
        self.assertNotIn(added_fieldset, original_admin.get_fieldsets(request))
        self.assertNotIn(added_inline, original_admin.tab_ressources)
        admin = TestBandAdmin(Band, self.site)
        inlines_classes = []
        inlines = admin.get_inline_instances(request)
        for inline in inlines:
            inlines_classes.append(inline.__class__)
        self.assertIn(added_inline, inlines_classes)
        self.assertIn(added_fieldset, admin.get_fieldsets(request))
        self.assertIn(added_fieldset, admin.get_fieldsets(request))

    def test_medias_method_with_default_settings(self):
        """
        Tests that the media method is retrning the proper static files when settings.TABBED_ADMIN_USE_JQUERY_UI
        is True or False.
        """
        self.assertEqual(False, USE_JQUERY_UI)
        admin = BandAdmin(Band, self.site)
        medias = admin.media
        self.assertEqual({}, medias._css)
        for js in medias._js:
            self.assertNotIn(js, 'tabbed_admin')

    def test_medias_method_with_grappelli(self):
        """
        Tests if the right css ile is triggered when grappelli is installed.
        """
        try:
            import grappelli
        except ImportError:
            return
        settings.INSTALLED_APPS += ('grappelli', )
        self.assertIn('grappelli', settings.INSTALLED_APPS)
        admin = BandAdmin(Band, self.site)
        medias = admin.media
        self.assertTrue(len(medias._css) > 0)
        self.assertIn('all', medias._css)
        self.assertTrue(len(medias._css['all']) == 1)
        self.assertIn('grappelli', medias._css['all'][0])
        

class TabbedAdminTagsTest(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.admin = BandAdmin(Band, self.site)
        self.req = request.get('/admin/tabbed_admin/tab/')
        self.req.user = request.user
        self.view = self.admin.add_view(self.req)
        self.context = Context(self.view)
        self.context.push()
        self.context['adminform'] = self.view.context_data['adminform']
        self.context['request'] = self.req
        self.context['inline_admin_formsets'] = self.view.context_data['inline_admin_formsets']

    def test_request_not_in_context_raising_improperly_configured(self):
        """
        Tests if an exception is thrown when no request is passed.
        """
        from django.core.exceptions import ImproperlyConfigured
        context = self.context
        del context['request']
        self.assertRaises(ImproperlyConfigured, render_tab_fieldsets_inlines, self.context, [])

    def test_fieldset_passed_returns_fieldset_templated(self):
        """
        Tests if the fieldset html is correctly generated when a fieldset is passed
        """
        fieldset = self.view.context_data['tabs']['fields'][0]['entries'][0]
        self.assertEqual('fieldset', fieldset['type'])
        #tag = render_tab_fieldsets_inlines(self.context, fieldset)
        #self.assertIn('fieldset', tag)

    def test_inline_passed_returns_inline_templated(self):
        """
        Tests if an inline html is correctly generated when an inline is passed.
        """
        inline = self.view.context_data['tabs']['fields'][0]['entries'][1]
        self.assertEqual('inline', inline['type'])
        #tag = render_tab_fieldsets_inlines(self.context, inline)
        #self.assertIn('inline', tag)

    def test_wrong_inline_key_returns_nothing(self):
        """
        Tests if a worng inline naming returns nothing.
        """
        inline = self.view.context_data['tabs']['fields'][0]['entries'][1]
        self.assertEqual('inline', inline['type'])
        inline['name'] = 'Not exists'
        tag = render_tab_fieldsets_inlines(self.context, inline)
        self.assertEqual('', tag)
