# -*- coding: utf-8 -*-
"""
@author: Coco
"""

def application(environ, start_response):
	start_response("200 OK", [('Content-Type', 'text/html')])
	return "<h1>Hello,world</h1>"