# This is a modified copy of \elastic\query.py

# now also playing around with these instructions for a BERT/elastic combo
# https://towardsdatascience.com/elasticsearch-meets-bert-building-search-engine-with-elasticsearch-and-bert-9e74bf5b4cf2

#Start query code
from elasticsearch import Elasticsearch
from elasticsearch_dsl.query import MultiMatch
from elasticsearch_dsl import Search, Q
from nltk import tokenize
from nltk.stem import PorterStemmer 
from nltk.stem.snowball import SnowballStemmer
#from bert_serving.client import BertClient

es = Elasticsearch()
ps = PorterStemmer() 
ss = SnowballStemmer("dutch", ignore_stopwords=True)
indexName='01-01-sites'
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
	return q.lower()#newq

def mlt(q, size=3):
	print('more like this ' + str(q))
	#stemming query terms
	newq = stemm(q)
	
	if len(q) > 0:
		s = Search(using=es, index=indexName)
		s = s.query(Q({"more_like_this": { 
			"fields": ["markdownbody"],
			"like":{
				"_index":indexName,
				"_id":q
			}}}))[0:int(size)]
		response = s.execute()
		print(response)
		#if this set is empty, it just kinda breaks
		#if(len(response) < 1):
		#	return "{ 'results':'empty'} "
		return jsonResultsURL(response, q)
	return "{'results': { 'numresults': 1, 'hits': {'title': 'No query'}}}"

#todo pseudocode for when we added the 'domain' and manual 'domaintitle' facets
#INTERFACE todo: adjust preview to show domaintitle per document. Remove More Like This from initial results. Add 'explore site' button below.
#WEBSERVER todo: perform query within this same domain. also add url routing/view
#INTERFACE todo: after loading initial results, add top 3 results below. let those have 'more like this' as working now. update numresults per domain

def query(q, start=0):
	#how many results per page
	size = 10
	
	#stemming query terms
	newq = stemm(q)
		
	print(q)
	print(newq)
	
	#if there's no query, query on a space (get all)
	if len(q) == 0:
		newq = "de het een"
	#emb = 24#bc.encode(q)
	
	# Lets make an aggregation
	# 'by_house' is a name you choose, 'terms' is a keyword for the type of aggregator
	# 'field' is also a keyword, and 'house_number' is a field in our ES index
	print('start test')
	
	
	s = Search(using=es, index=indexName).query("multi_match", query = newq, fields = ["title", "url", "markdownbody"])
	
#	s = Search(using=es, index=indexName, )
	
	#size 0 = search all domains
	#s.aggs.bucket('by_domain', 'terms', field='domain.keyword', size=10)
	#s.execute()
	
	#print(s.aggregations.by_domain.doc_count)
	#print(s.hits.total)
	#print(s.aggregations.by_domain.buckets)
	
	#s = Search(using=es, index=indexName).query("multi_match", query = "").script(source=cosineSimilarity(params.queryVector, doc['embedding'])).params(queryVector=emb)#, params = "queryVector":emb
	#, script = {			"source":"cosineSimilarity(params.queryVector, doc['embedding'])",			"params": {"queryVector":emb}			})
	
	
	s2 = s[int(start):int(start)+size]
	#s.query(MultiMatch(query=q, fields=['title,', 'url', 'html']))
	response = s2.execute()
#	for hit in response:
#		print(hit)
	#.to_dict()
	
	
	#print(response.aggregations.by_domain.buckets[0])
	#for item in response.aggregations.by_domain.buckets:
	#	print(item.key)
	#	print(item.doc_count)
	#print(response)
	#print(response[0]['domain'])
	#print(response[8]['domain'])
#	print(response[2])
#	print(response[3])
	return response
#	return 'No query'

#TODO smarter document surrogate/preview here
def firstSentence(fulltext, q):

	lowlimit = 20
	highlimit = 40

	# Find the first sentence with a whitespace (i.e. not a URL)
	# and all query terms
	sentences = tokenize.sent_tokenize(fulltext)
	
	# kind of ugly way to see if a keywords is in this sentence..
	for sentence in sentences:
		sentence = sentence.lower()
		#highlight all regular words, or stemmed words
		keywords = q.lower().split(" ")+stemm(q).lower().split(" ")[0:-1]  #remove trailing space
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
	#if(response == 'No query'):
	#print(response)
	if len(response) == 0:
		res['numresults'] = '0 results\n\n'
	else:
#		print()
#		response_dict = json.loads(response.content)
#		for key, v in response_dict:
#			print(key)
		for hit in response:
#			print()
#			print(test)
			#print('NEWRESULT')
			#print()
			#breakpoint()
			#print(hit.meta['id'])
#			res += hit['title'] + '\n'
#			res += hit['url'] + '\n'
			res['hits'].append({
				'title':hit['title'],
				'url':hit['url'],
				'preview': firstSentence(hit['markdownbody'], q),#strip_tags(
				'markdownbody':hit['markdownbody'],
				'docid':hit.meta['id'],
				'domain':hit['domain'],
				'theme':hit['theme']
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





