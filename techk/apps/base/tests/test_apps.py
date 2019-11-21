# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import SimpleTestCase

from ..apps import BaseConfig


class AppConfigTestCase(SimpleTestCase):

    def test_ready(self):
        from django.apps.registry import apps

        base_app_config = apps.app_configs['base']
        app_config = BaseConfig(
            app_name=base_app_config.name,
            app_module=base_app_config.module,
        )

        # Nothing should be raised.
        app_config.ready()
