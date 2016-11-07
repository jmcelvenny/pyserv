#!/usr/bin/python
import hashlib

def onPageLoad(paramstr):
	params = {}

	if (paramstr is ""):
		return "No parameters specified"

	p = paramstr.split("&")
	for s in p:
		k = s.split("=")
		if (len(k) is not 2):
			return "Invalid parameter: %s" % s

		params[k[0]] = k[1]

	if (params['user'] == "" or params['pass'] == ""):
		return "Invalid parameters: %s" % params

	return "Username: "+params['user']+"</br>Password Hash: "+str(hashlib.sha224(params['pass']).hexdigest())