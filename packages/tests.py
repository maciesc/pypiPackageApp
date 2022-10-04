import elastic_transport
from django.test import TestCase

from packages.jobs import download_and_index_packages
from packages.models import Package
from django.test import Client
from unittest.mock import patch
from parameterized import parameterized


class PackageModel(TestCase):
    def test_creates_and_save_package_from_dict_data(self):
        package = {
            "name": "test",
            "author": "",
            "author_email": "",
            "description": "test",
            "keywords": "",
            "version": "0.0.2",
            "maintainer": "",
            "maintainer_email": "",
        }
        p = Package(**package)
        p.save()

        for key in package.keys():
            assert getattr(p, key) == package[key]

        assert Package.objects.count() == 1


ELASTIC_NOT_FOUND_RETURN_VALUE = {
    "took": 0,
    "timed_out": False,
    "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
    "hits": {"total": {"value": 0, "relation": "eq"}, "max_score": None, "hits": []},
}

ELASTIC_FOUND_PACKAGE_RETURN_VALUE = {
    "took": 0,
    "timed_out": False,
    "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
    "hits": {
        "total": {"value": 1, "relation": "eq"},
        "max_score": None,
        "hits": [
            {
                "_index": "pypi-packages",
                "_id": "test",
                "_score": 1,
                "_source": {
                    "name": "test",
                    "author": "test_author",
                    "author_email": "test_author_email",
                    "description": "",
                    "keywords": "",
                    "version": "0.1.0",
                    "maintainer": "",
                    "maintainer_email": "",
                },
            },
        ],
    },
}


class PackagesListView(TestCase):
    @parameterized.expand(
        [
            "/",
            "/?query=test",
        ]
    )
    @patch("packages.views.ES_CLIENT")
    def test_renders_empty_packages_list_when_elastic_search_client_returns_no_data(
        self, path, es_client
    ):
        es_client.search.return_value = ELASTIC_NOT_FOUND_RETURN_VALUE
        client = Client()
        response = client.get(path)

        assert response.status_code == 200
        self.assertQuerysetEqual(response.context["packages"].object_list, [])

    @parameterized.expand(
        [
            "/",
            "/?query=test",
        ]
    )
    @patch("packages.views.ES_CLIENT")
    def test_renders_packages_list_when_elastic_search_client_returns_package_data(
        self, path, es_client
    ):
        es_client.search.return_value = ELASTIC_FOUND_PACKAGE_RETURN_VALUE
        client = Client()
        response = client.get(path)

        assert response.status_code == 200
        self.assertQuerysetEqual(
            response.context["packages"].object_list,
            [
                {
                    "name": "test",
                    "author": "test_author",
                    "author_email": "test_author_email",
                    "description": "",
                    "keywords": "",
                    "version": "0.1.0",
                    "maintainer": "",
                    "maintainer_email": "",
                }
            ],
        )

    @parameterized.expand(
        [
            "/",
            "/?query=test",
        ]
    )
    @patch("packages.views.ES_CLIENT")
    def test_renders_empty_packages_list_from_database_when_elastic_search_client_throws_error(
        self, path, es_client
    ):
        es_client.search.side_effect = elastic_transport.ConnectionError(message="test")
        client = Client()
        response = client.get(path)

        assert response.status_code == 200
        self.assertQuerysetEqual(
            response.context["packages"].object_list,
            [],
        )

    @parameterized.expand(
        [
            "/",
            "/?query=test",
        ]
    )
    @patch("packages.views.ES_CLIENT")
    def test_renders_packages_list_from_database_when_elastic_search_client_throws_error(
        self, path, es_client
    ):
        db_package = Package(name="test")
        db_package.save()
        es_client.search.side_effect = elastic_transport.ConnectionError(message="test")
        client = Client()
        response = client.get(path)

        assert response.status_code == 200
        self.assertQuerysetEqual(
            response.context["packages"].object_list,
            [db_package],
        )


class JsonNewestPackagesView(TestCase):

    @patch("packages.views.pypi_rss")
    def test_returns_json_newest_packages(
        self, pypi_rss
    ):
        pypi_package = [{'title': 'test', 'link': 'https://pypi.org/project/ctlog/', 'guid': 'https://pypi.org/project/ctlog/', 'description': 'SAT', 'author': None, 'pubdate': '2022-10-04 13:18:44', 'name': 'ctlog'}]
        pypi_rss.get_newest_packages.return_value = pypi_package
        client = Client()
        response = client.get("/newest_packages")

        assert response.status_code == 200
        assert response.headers.get('content-type') == 'application/json'
        assert response.json() == pypi_package


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class Jobs(TestCase):
    @patch("packages.jobs.pypi_rss")
    @patch("packages.jobs.requests")
    @patch("packages.jobs.ES_CLIENT")
    def test_download_and_index_packages(self, es_client, requests, pypi_rss):
        pypi_rss.get_newest_packages.return_value = [{"name": "test"}]
        pypi_api_response = {
            "info": {
                "author": "test",
                "author_email": "test.mail@gmail.com",
                "description": "",
                "keywords": "",
                "maintainer": "",
                "maintainer_email": "",
                "name": "python-test",
                "version": "0.1.1",
            },
        }
        requests.get.return_value = MockResponse(pypi_api_response, 200)
        es_client.index.return_value = {}
        download_and_index_packages()

        es_client.index.assert_called_once()
        assert Package.objects.count() == 1
