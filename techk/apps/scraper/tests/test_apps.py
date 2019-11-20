# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import SimpleTestCase

from ..apps import ScraperConfig


class AppConfigTestCase(SimpleTestCase):

    def test_ready(self):
        from django.apps.registry import apps

        scraper_app_config = apps.app_configs['scraper']
        app_config = ScraperConfig(
            app_name=scraper_app_config.name,
            app_module=scraper_app_config.module,
        )

        # Nothing should be raised.
        app_config.ready()
