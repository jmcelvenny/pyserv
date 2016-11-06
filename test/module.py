#!/usr/bin/python

#####PYTHON PAGE FORMAT
# GET /test/module.py?user=bob&pass=jones HTTP/1.1
# The file /test/module.py has method onPageLoad() imported
# onPageLoad(user=bob&pass=jones) is invoked
# onPageLoad() returns a string: the contents of the webpage.
#####

def onPageLoad(params):
	return "module successfully run"	
