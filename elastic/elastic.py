# trying out search/morelikethis
from elasticsearch import Elasticsearch
es = Elasticsearch()

#query on the html field using the keyword 'ouderen'
res = es.search(index="23-12-sites", body=
	{ "query": 
		{"match": 
			{"html": "ouderen"}
		}
	})

print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
	print(hit['_source']['url'])
	
print('\n')
print('Lets try to find more like: ' + str(res['hits']['hits'][0]['_source']['url']))


# We compare the contents of the html field now to find something similar

# A bit hacky.. we now use the DSL version of elasticsearch. This one's 
# supposed to be a bit easier to use, so I wanted to see if it's easier
# to define a query with this syntax (compared to above)

from elasticsearch_dsl.query import MoreLikeThis
from elasticsearch_dsl import Search

#html my_text = str(res['hits']['hits'][0]['_source']['html'])
my_text = str(res['hits']['hits'][0]['_source']['url'].replace('/',' ').replace('-', ' ')) #url

s = Search(using=es)
s = s.query(MoreLikeThis(like=my_text, fields=['url', 'html', 'title']))
# You can also exclude fields from the result to make the response quicker in the normal way
# s = s.source(exclude=["sentences", "text"])
response = s.execute().to_dict()
print('There are ' + str(response['hits']['total']['value']) + ' results:\n')
for i in range (0,5):
	print(response['hits']['hits'][i]['_source']['url'])
	
#The recommendation probably works terrible because it now also compares html tags