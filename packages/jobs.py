import elastic_transport
import pypi_rss
from django.db import IntegrityError

from packages.models import Package
from pypiPackageApp.settings import ES_CLIENT, INDEX_NAME


def download_and_index_packages():
    print("starting downloading and indexing packages")
    packages = pypi_rss.get_newest_packages()
    _index_packages_in_elastic(packages)
    _index_packages_in_db(packages)
    print("finished indexing")


def _index_packages_in_elastic(packages):
    for package in packages:
        try:
            ES_CLIENT.index(
                index=INDEX_NAME,
                id=package["name"],
                document=package,
            )
        except (ValueError, elastic_transport.ConnectionError):
            print('There is a problem with elastic cloud client')
            break


def _index_packages_in_db(packages):
    for package in packages:
        try:
            p = Package(**package)
            p.save()
        except IntegrityError:
            pass
