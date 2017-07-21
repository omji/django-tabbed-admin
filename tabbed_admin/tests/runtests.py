import os
import sys


from django.conf import settings

DIRNAME = os.path.dirname(__file__)
settings.configure(
    DEBUG=True,
    DATABASE_ENGINE='sqlite3',
    DATABASE_NAME=os.path.join(DIRNAME, 'database.db'),
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3'
        }
    },
    ROOT_URLCONF='tabbed_admin.tests.urls',
    MIDDLEWARE_CLASSES=(),
    TEMPLATE_CONTEXT_PROCESSORS=[
        'django.template.context_processors.request'
    ],
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth'
                ],
            },
        },
    ],
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',

        'tabbed_admin',
        'tabbed_admin.tests'
    )
)


try:
    # Django < 1.8
    from django.test.simple import DjangoTestSuiteRunner
    test_runner = DjangoTestSuiteRunner(verbosity=1)
except ImportError:
    # Django >= 1.8
    from django.test.runner import DiscoverRunner
    test_runner = DiscoverRunner(verbosity=1)

try:
    # Django < 1.7
    from django.core.management import setup_environ
    setup_environ(settings)
    failures = test_runner.run_tests(['tabbed_admin'])
except:
    # Django >= 1.7
    import django
    django.setup()

if __name__ == "__main__":
    from django.test.utils import get_runner
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tabbed_admin.runtests'
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['tabbed_admin'])

if failures:
    sys.exit(failures)
