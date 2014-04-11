
halt_when() {
    if [ $? != 0 ]; then
        echo $@ 1>&2;
        exit $?
    fi
}

source `which virtualenvwrapper.sh`
halt_when "importing virtualenvwrapper failed."

rmvirtualenv bookstore # ignore failure

mkvirtualenv -p `which python2.7` bookshare
halt_when "creating virtualenv failed."

pip install -r requirements/base.txt
halt_when "installing dependency failed."