# pypiPackageApp

This app is simple django application that once per day at 00:00 (UTC) downloads newest pypi packages, and store data package fields:
name, author, author email,version, maintainer, maintainer email, description, keywords
in elastic search cloud, and in local database. It allows you to search these packages using a simple query search engine.

To create a connection to elastic cloud you must add elastic.ini file in the main application directory like so:
```ini
[ELASTIC]
cloud_id = your_google_cloud_id
user = elastic_user
password = elastic_password
```

Project uses poetry to install all packages and dependencies,
depending on the system that you work you can create environment using the documentation
https://python-poetry.org/docs/

To run project localy open project main application directory in the system command line and type:
```
python manage.py runserver
```

Pagination depends on enviroment variable ITEMS_PER_PAGE which means how many packages will be listed in one page and if there is no configuration of this variable the default value will be 10.
