# using the sites.json, we use the python bulk helper to index these files in elastic
# https://elasticsearch-py.readthedocs.io/en/master/helpers.html

# Windows install: first install and start elastic (bin/elastic.bat)
# Also pip install elasticsearch (for the python libraries), and bigjson
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
from annotatetheme import annotatecontent
#import bigjson
from urllib.parse import urlparse



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
from pathlib import Path
import json
from time import sleep

indexName = '01-01-sites'
indexFile = '23-12-2-sites.json'

print(Path.cwd())

def gendata():
	i = 0 #number of files indexed
	j = 0
	z = 0
	with open(Path.cwd() / indexFile) as f:
#		j = bigjson.load(f)
		#for i in range(0, len(j)):
		
		for line in f:
			print(i)
			if(len(line) > 2):
				#first everything after the object definition (usually comma's and whitespaces)
				while(line[-1] != '}'):
					line = line[0:-1]
				if(len(line) > 5):
					z+=1
				#For the json.reads file to work, it needs to understand this line is only 1 object
				prepline = '{"doc":' + line + '}'
#				print(prepline)
				jsline = json.loads(prepline)

			#for each item
			#for jsline in fjson:
#		jsline = json.loads(obj)
				yield {
					"_index": indexName,
					"_type":"document",
					"_source": {
						"url":jsline['doc']['url'],
						"title":jsline['doc']['title'],
						"keywords":jsline['doc']['keywords'],
						"markdownbody":jsline['doc']['markdownbody'],
						"html":jsline['doc']['html'],
						"urls":jsline['doc']['urls'],
						"theme":annotatecontent(jsline['doc']['markdownbody']),
						"domain": urlparse(jsline['doc']['url']).netloc#{
						#	"_type": "keywords",
						#	"_source": urlparse(jsline['doc']['url']).netloc
						#}
					}
				}
				i+=1
			j+=1
	print()
	print(i)
	print(j)
	print(z)


#connect to ES
es = Elasticsearch(timeout=30, max_retries=10, retry_on_timeout=True)
es.indices.create(index=indexName, ignore=400)
#perform bulk index
bulk(es, gendata())