#!/usr/bin/env python

import random

secret = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))
print "export BOOKSHARE_SECRET_KEY='{}'".format(secret)
