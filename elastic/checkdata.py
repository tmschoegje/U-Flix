# based on prep.py - used to count some statistics


# how many external urls
# how many documents per domain
# make a dictionary w/ key 'domain', and value urls 

from pathlib import Path
import json
from time import sleep
from urllib.parse import urlparse

indexFile = '23-12-2-sites.json'

print(Path.cwd())

domaindict = dict([])
outgoingdict = dict([])
outlist = []

def buildDict(domdict, outdict, outlst):
	with open(Path.cwd() / indexFile) as f:
		for line in f:
			if(len(line) > 2):
				#first everything after the object definition (usually comma's and whitespaces)
				while(line[-1] != '}'):
					line = line[0:-1]
				#For the json.reads file to work, it needs to understand this line is only 1 object
				prepline = '{"doc":' + line + '}'
#				print(prepline)
				jsline = json.loads(prepline)

			#for each item
			#for jsline in fjson:
#		jsline = json.loads(obj)


				#test if exists
				dom = urlparse(jsline['doc']['url']).netloc
				
				if (dom in domdict):
					domdict[dom].append(jsline['doc']['url'])
				else:
					domdict[dom] = [jsline['doc']['url']]
				for urly in jsline['doc']['urls']:
					outlst.append(urly)
					print(urly)
					dom2 = urlparse(urly).netloc
					if(dom2 in outdict):
						outdict[dom2].append(urly)
					else:
						outdict[dom2] = [urly]
print()
print(str(outgoingdict)[0:100])
buildDict(domaindict, outgoingdict, outlist)
print('Domaindict has ' + str(len(domaindict)) + ' keys')
#for dom in domaindict:
#	print(str(dom) + ' ' + str(domaindict[dom]))
print('Outgoingdict has ' + str(len(outgoingdict)) + ' domains')
print('Outlist has ' + str(len(set(outlist))))

with open('domdict.txt', 'w') as file:
	for dom in domaindict:
		file.write(str(dom) + ' has ' + str(len(domaindict[dom])) + ' pages\n')  #TODO count how many are not plaintext stuff
alloutdoms = set()
with open('outdict.txt', 'w') as file:
	for dom in outgoingdict:
		alloutdoms.union(set(outgoingdict[dom]))
	for dom in alloutdoms:
		file.write(str(dom) + '\n')
#     file.write(json.dumps(outgoingdict))
with open('outlist.txt', 'w') as file:
	for url in set(outlist):
		file.write(str(url) + '\n')