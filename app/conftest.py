import django
from django.conf import settings


# `pytest` automatically calls this function once when tests are run.
def pytest_configure():
    settings.DEBUG = False
    django.setup()


def pytest_unconfigure():
    pass
