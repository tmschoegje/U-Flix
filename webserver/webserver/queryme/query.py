# This is a modified copy of \elastic\query.py

# now also playing around with these instructions for a BERT/elastic combo
# https://towardsdatascience.com/elasticsearch-meets-bert-building-search-engine-with-elasticsearch-and-bert-9e74bf5b4cf2

#Start query code
from elasticsearch import Elasticsearch
from elasticsearch_dsl.query import MultiMatch
from elasticsearch_dsl import Search
from nltk import tokenize
from nltk.stem import PorterStemmer 
from nltk.stem.snowball import SnowballStemmer
#from bert_serving.client import BertClient

es = Elasticsearch()
ps = PorterStemmer() 
ss = SnowballStemmer("dutch", ignore_stopwords=True)
indexName='24-12-urls-sites'
#indexName="25-12-sites"
#bc = BertClient(output_fmt='list')

#s = Search(using=es, index='sites3')

def qry(q, start=1):
#	print('START HERE')
#	print(start)
	return jsonResultsURL(query(q, start),q)

#Currently not stemming - e.g. 'eenzaam' would be stemmed and give no results
#Should probably query, and then re-query with stemming
#I think elastic has some stemming function too. Or maybe during indexing already stem all words?
def stemm(q):
	splitq = q.split(" ")
	newq = ""
	for qterm in splitq:
		newq += ss.stem(qterm) + " "
	return q#newq

def query(q, start=0):
	#how many results per page
	size = 10
	
	#stemming query terms
	newq = stemm(q)
		
	print(q)
	print(newq)
	
	if len(q) > 0:
		#emb = 24#bc.encode(q)
		s = Search(using=es, index=indexName).query("multi_match", query = newq, fields = ["title", "url", "markdownbody"])
		#s = Search(using=es, index=indexName).query("multi_match", query = "").script(source=cosineSimilarity(params.queryVector, doc['embedding'])).params(queryVector=emb)#, params = "queryVector":emb
		#, script = {			"source":"cosineSimilarity(params.queryVector, doc['embedding'])",			"params": {"queryVector":emb}			})
		s2 = s[int(start):int(start)+size]
		#s.query(MultiMatch(query=q, fields=['title,', 'url', 'html']))
		response = s2.execute()
#	for hit in response:
#		print(hit)
	#.to_dict()
		return response
	return 'No query'

#TODO smarter document surrogate/preview here
def firstSentence(fulltext, q):

	lowlimit = 20
	highlimit = 40

	# Find the first sentence with a whitespace (i.e. not a URL)
	# and all query terms
	sentences = tokenize.sent_tokenize(fulltext)
	
	# kind of ugly way to see if a keywords is in this sentence..
	for sentence in sentences:
		#highlight all regular words, or stemmed words
		keywords = q.split(" ")+ stemm(q).split(" ")[0:-1]  #remove trailing space
		#print(keywords)
		
		hits = 0
		for keyword in keywords:
			if keyword in sentence:
				hits += 1
		if hits > 0:#== len(keywords):   Could test if all keywords are in the sentence
			# we're going to return this sentence. return the keywords,
			# the words in front and behind
			splitsent = sentence.split(" ")
			
			#possible TODO: first check if there's an unstemmed match - else find a stemmed match
			returnsent = ""
			returnsentend = ""
			for index, word in enumerate(splitsent):
				if word in keywords:
					if index < lowlimit:
						lowlimit = index
					else:
						returnsent += ".. "
					if not (len(splitsent) < index + highlimit):
						returnsentend += " .."
					return returnsent + " ".join(splitsent[index - lowlimit:index]) + ' <b>' + splitsent[index] + '</b> ' + " ".join(splitsent[index + 1:index + highlimit]) + returnsentend
				
#		if (q.split(" ")[0] in sentence):
#			return sentence
#		for x in q.split(" "):
#			if x not in sentence:
#				break
		# If we didn't get interrupted, return this sentence
#		print('golden sentence here!')
#		print(sentence)
#		return sentence
	return "No preview available."
	
	# Return the 10 words before and 10 after
	
#				print(x)
		#print('END')
	
	
		#If all query words occur in the sentence
		#print( [x in sentence for x in q.split(" ")])
#		if(all([x in sentence for x in q.split(" ")])):
#			print('\n\n\n\nstart')
#			print(re.sub(" +", " ", sentence.replace("\n", "").replace("\r", "")))
#			print('end')
#			return re.sub(" +", " ", sentence)
#	return 'No preview'


#This one is for testing stuff on the webserver!
def stringResultsURL(response, q):
	res = "> " + q + "\n"
	#Test if there are results
	if len(response) == 0:
		res += '0 results\n\n'
	else:
		for hit in response:
			#print('NEWRESULT')
			#print()
			#print(hit)
			#breakpoint()
			res += hit['title'] + '\n'
			res += hit['url'] + '\n'
#		print(hit['title'])
#		print(hit['url'])
		#strip the html content
#		print(firstSentence(strip_tags(hit['html']), q))
			res += firstSentence(hit['markdownbody'], q) + '\n\n'  #from nltk import tokenize(hit
	return res

#This one is claled by the interface!
def jsonResultsURL(response, q):
	
	res = {
		'query': q,#"> " + q + "\n"
		'hits': [],
		}
	#Test if there are results
	if len(response) == 0:
		res['numresults'] = '0 results\n\n'
	else:
		for hit in response:
			#print('NEWRESULT')
			#print()
			#print(hit)
			#breakpoint()
#			res += hit['title'] + '\n'
#			res += hit['url'] + '\n'
			res['hits'].append({
				'title':hit['title'],
				'url':hit['url'],
				'preview': firstSentence(hit['markdownbody'], q),#strip_tags(
				'markdownbody':hit['markdownbody']
			})
		#print(response)
		res['numresults'] = response.hits.total.value#len(response)
			
#		print(hit['title'])
#		print(hit['url'])
		#strip the html content
#		print(firstSentence(strip_tags(hit['html']), q))
	return res

def printResultsURL(response, q):
	print(stringResultsURL(response, q))

		
#		firstSentence(tokenize.sent_tokenize(strip_tags(hit['html'])), q)
		
		
	#print(response)
#	time.sleep(600)
#	for hit in response:
#		print(hit)

#	res = response['hits']
	
#	print(str(res['total']['value']) + ' results\n')
#	for hit in response:#range (0,5):
#		print(hit)
#		print(res['hits'][i]['_source']['url'])
#		print(res['hits'][i]['_score'])
#		print(firstSentence(tokenize.sent_tokenize(strip_tags(res['hits'][i]['_source']['html'])), q))

#q = 'tivoli'
#printResultsURL(query(q), q)

#q = 'utrecht'
#printResultsURL(query(q), q)

#q = 'ouderen'
#printResultsURL(query(q), q)





