import logging

from django.core.management.commands import test


logger = logging.getLogger(__name__)


class Command(test.Command):
    def handle(self, *args, **options):
        logger.error('Use pytest command instead of manage.py test')
