
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


echo -e "\033[32m [SUCCESS] \033[0m Setup done! Follow the remaining steps."
