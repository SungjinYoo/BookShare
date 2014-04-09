
source `which virtualenvwrapper.sh`
if [ $? != 0 ]; then
  printf "importing virtualenvwrapper failed."
  exit $?
fi

rmvirtualenv bookstore # ignore failure

mkvirtualenv -p `which python2.7` bookshare
if [ $? != 0 ]; then
  printf "creating virtualenv failed."
  exit $?
fi

pip install -r requirements/base.txt
if [ $? != 0 ]; then
  printf "installing dependency failed."
  exit $?
fi
