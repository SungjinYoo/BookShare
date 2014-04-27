
halt_when_fail() {
    if [ $? != 0 ]; then
        echo -e "\033[31m [FAIL] \033[0m"$@ 1>&2;
        exit $?
    fi
}

source `which virtualenvwrapper.sh`
halt_when_fail "importing virtualenvwrapper"

rmvirtualenv bookstore # ignore failure

mkvirtualenv -p `which python2.7` bookshare
halt_when_fail "creating virtualenv"

pip install -r requirements/base.txt
halt_when_fail "installing dependency"

`python keygen.py`

pushd bookshare/apps
APPS=$(find * ! -path . -maxdepth 1 -type d)
popd


for app in $APPS
do
    python manage.py schemamigration --initial $app
    halt_when_fail "schema migration for $app"
done

python manage.py syncdb
halt_when_fail "syncdb"

for app in $APPS
do
    python manage.py migrate $app
    halt_when_fail "data migration"
done

echo -e "\033[32m [SUCCESS] \033[0m Setup done! Follow the remaining steps."