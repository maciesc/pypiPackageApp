from typing import Dict
import json
import elastic_transport
import pypi_rss
from django.shortcuts import render
from django.db.models import Q

from pypiPackageApp.settings import ES_CLIENT, INDEX_NAME, ITEMS_PER_PAGE
from .models import Package

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse


def packages_list(request):
    query = request.GET.get("q")
    elastic_query = __create_elastic_query(query)
    try:
        elastic_response = ES_CLIENT.search(
            index=INDEX_NAME, query=elastic_query, size=10000
        )
    except (ValueError, elastic_transport.ConnectionError):
        packages = __get_packages_queryset_by_query(query)
    else:
        packages = [hit["_source"] for hit in elastic_response["hits"]["hits"]]

    paginator = Paginator(packages, ITEMS_PER_PAGE)

    page = request.GET.get("page")
    try:
        packages = paginator.page(page)
    except PageNotAnInteger:
        packages = paginator.page(1)
    except EmptyPage:
        packages = paginator.page(paginator.num_pages)

    context = {"packages": packages}
    return render(request, "packages-list.html", context)


def __create_elastic_query(query: str) -> Dict:
    if query:
        return {
            "bool": {
                "should": [
                    {"match": {"name": {"query": query, "operator": "and"}}},
                    {"match": {"author": {"query": query, "operator": "and"}}},
                    {"match": {"author_email": {"query": query, "operator": "and"}}},
                    {"match": {"description": {"query": query, "operator": "and"}}},
                    {"match": {"version": {"query": query, "operator": "and"}}},
                    {"match": {"maintainer": {"query": query, "operator": "and"}}},
                    {
                        "match": {
                            "maintainer_email": {"query": query, "operator": "and"}
                        }
                    },
                    {"match": {"keywords": {"query": query, "operator": "and"}}},
                ],
                "minimum_should_match": 1,
            }
        }
    else:
        return {"match_all": {}}


def __get_packages_queryset_by_query(query):
    if query:
        return Package.objects.filter(
            Q(name__icontains=query)
            | Q(author_email__icontains=query)
            | Q(description__icontains=query)
            | Q(keywords__icontains=query)
            | Q(version__icontains=query)
            | Q(maintainer__icontains=query)
            | Q(maintainer_email__icontains=query)
        ).distinct()
    else:
        return Package.objects.all()


def json_newest_packages(request):
    response_data = pypi_rss.get_newest_packages()
    return HttpResponse(json.dumps(response_data, default=str), content_type="application/json")
