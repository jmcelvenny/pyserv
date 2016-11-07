#!/usr/bin/python

import datetime
import time


def onPageLoad(paramstr):
	now = datetime.datetime.now()
	return "Current Time: " + now.strftime("%c")
