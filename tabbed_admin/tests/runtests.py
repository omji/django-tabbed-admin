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
    MIDDLEWARE_CLASSES=(),
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

failures = test_runner.run_tests(['tabbed_admin'])
if failures:
    sys.exit(failures)
