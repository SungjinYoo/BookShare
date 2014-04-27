BookShare
=========

Hanyang Univ. book sharing system


Dependency
----------
- Python 2.7
- virtualenvwrapper

Installation
------------
1. Do `bash setup.sh` from project root directory.
2. Do `./keygen.py` and append the text to `activate` script.
3. Do `workon bookstore`.
4. Do `./manage.py runserver` from project root directory.
5. Profit!

Standard Migration Workflow
---------------------------
1. Change model.
2. `python manage.py schemamigration --auto <app name>` for schema change.
3. `python manage.py migrate <app name>` for data change.
