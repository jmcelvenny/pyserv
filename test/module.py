#!/usr/bin/python

#####PYTHON PAGE FORMAT
# GET /test/module.py?user=bob&pass=jones HTTP/1.1
#
# Server imports module.py's onPageLoad method
# onPageLoad(user=bob&pass=jones) is called
# onPageLoad() returns a string: the contents of the webpage.
#
# Side Note: 	Python requires that an __init__.py file exist in the directory of the .py file
#		This is to ensure safe imports. Not necessary if the .py is the same directory as server.py
#####

def onPageLoad(params):
	return "module successfully run"	
