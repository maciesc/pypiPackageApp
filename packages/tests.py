from datetime import datetime

from django.test import TestCase

from packages.models import Package


class PackageTestCase(TestCase):
    def test_creates_and_save_package_from_dict_data(self):
        package = {
            "title": "nonebot-plugin-lisenter added to PyPI",
            "link": "https://pypi.org/project/nonebot-plugin-lisenter/",
            "guid": "https://pypi.org/project/nonebot-plugin-lisenter/",
            "description": "test_description",
            "author": "test_author",
            "pubdate": datetime(2022, 9, 29, 17, 19, 43),
            "name": "nonebot-plugin-lisenter",
        }
        p = Package(**package)
        p.save()

        for key in package.keys():
            assert getattr(p, key) == package[key]

        assert Package.objects.count() == 1