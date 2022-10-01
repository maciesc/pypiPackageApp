import elastic_transport
from django.shortcuts import render
from django.db.models import Q

from pypiPackageApp.settings import ES_CLIENT, INDEX_NAME
from .models import Package

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def packages_list(request):
    packages = Package.objects.all()
    query = request.GET.get("q")
    if query:
        elastic_query = {
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
        try:
            response = ES_CLIENT.search(
                index=INDEX_NAME, query=elastic_query, size=10000
            )
        except (ValueError, elastic_transport.ConnectionError):
            packages = Package.objects.filter(
                Q(name__icontains=query)
                | Q(author_email__icontains=query)
                | Q(description__icontains=query)
                | Q(keywords__icontains=query)
                | Q(version__icontains=query)
                | Q(maintainer__icontains=query)
                | Q(maintainer_email__icontains=query)
            ).distinct()
        else:
            packages = [hit["_source"] for hit in response["hits"]["hits"]]

    paginator = Paginator(packages, 6)
    page = request.GET.get("page")

    try:
        packages = paginator.page(page)
    except PageNotAnInteger:
        packages = paginator.page(1)
    except EmptyPage:
        packages = paginator.page(paginator.num_pages)

    context = {"packages": packages}
    return render(request, "packages-list.html", context)
