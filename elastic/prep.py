# using the sites.json, we use the python bulk helper to index these files in elastic
# https://elasticsearch-py.readthedocs.io/en/master/helpers.html

# Windows install: first install and start elastic (bin/elastic.bat)
# Also pip install elasticsearch (for the python libraries)
# Get sites.json from the spider, and then do this. Note: I hardcoded a link that should be changed



# deprecated:
# The elastic bulk API wants a certain format, so we prepare 
# the data for that: 1 line says the elastic operation (index),
# the next says the webpage we index
# https://www.elastic.co/guide/en/elasticsearch/reference/7.4/docs-bulk.html
# It also complained about some chars in html (such as parentheses), so I just strip those for now

import os
import sys
import re 




#f = open("C:\\Users\\tmsch\\Desktop\\elastic\\sites.json")
#copy = open("C:\\Users\\tmsch\\Desktop\\elastic\\sites2.json","wt")\

# the copying
#for line in f:
#	copy.write("{ \"index\" : { \"_index\" : \"sites\" } }\n")
	#copy.write(strip_tags(line))
#	copy.write(line)
	
#elastic expects a newline at the end
#copy.write("\n")


from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
from time import sleep

def gendata():
	f = open("C:\\Users\\tmsch\\Desktop\\werk\\uflix\\elastic\\sites.json")
	fjson = json.load(f)

	#for each item
	for jsline in fjson:
#		jsline = json.loads(obj)
		yield {
			"_index": "sites3",
			"_type":"document",
			"url":jsline['url'],
			"title":jsline['title'],
			"keywords":jsline['keywords'],
			"html":jsline['html']
		}

#connect to ES
es = Elasticsearch()
#perform bulk index
bulk(es, gendata())