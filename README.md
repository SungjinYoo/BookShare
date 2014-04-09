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
2. Append `export BOOKSHARE_SECRET_KEY='<your key>'` to the `activate` script.  
   Get a key from [Django Secret Key Generator](http://www.miniwebtool.com/django-secret-key-generator/)
3. Do `./manage.py syncdb`.
