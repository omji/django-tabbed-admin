from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from tabbed_admin.tests.admin import BandAdmin, InterviewInline
from tabbed_admin.tests.models import Band


class MockRequest(object):
    pass


class MockSuperUser(object):
    def has_perm(self, perm):
        return True

request = MockRequest()
request.user = MockSuperUser()


class TabbedModelAdminTest(TestCase):

    def setUp(self):
        self.band = Band()
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
        self.assertIn(added_fieldset, admin.get_fieldsets(request))
