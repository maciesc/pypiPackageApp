import elastic_transport
import pypi_rss
import requests
from django.db import IntegrityError

from packages.models import Package
from pypiPackageApp.settings import ES_CLIENT, INDEX_NAME


def download_and_index_packages():
    print("starting downloading and indexing packages")
    packages = pypi_rss.get_newest_packages()
    for package in packages:
        response = requests.get(f"https://pypi.org/pypi/{package['name']}/json")

        if response.status_code == 200:
            info = response.json()["info"]
            package_data = {
                "name": info["name"],
                "author": info["author"],
                "author_email": info["author_email"],
                "description": info["description"],
                "keywords": info["keywords"],
                "version": info["version"],
                "maintainer": info["maintainer"],
                "maintainer_email": info["maintainer_email"]
            }

            _index_package_in_elastic(package_data)
            _index_package_in_db(package_data)

    print("finished indexing")


def _index_package_in_elastic(package_data: dict):
    try:
        ES_CLIENT.index(
            index=INDEX_NAME,
            id=package_data["name"],
            document=package_data,
        )
    except (ValueError, elastic_transport.ConnectionError):
        print('There is a problem with elastic cloud client')


def _index_package_in_db(package_data: dict):
    try:
        Package.objects.update_or_create(name=package_data["name"], defaults=package_data)
    except IntegrityError:
        pass
