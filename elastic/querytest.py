from elasticsearch import Elasticsearch
from elasticsearch_dsl.query import MultiMatch
from elasticsearch_dsl.query import Match
from elasticsearch_dsl import Search

es = Elasticsearch()
s = Search(using=es, index='sites3').query("multi_match", query ="ouderen", fields = ["title", "url", "html"])

#response = s.scan()
#for res in response:
#	print(res)
#s.query(Match(query='ouderen'))
response = s.execute()#.to_dict()
#print(response['hits']['total']['value'])
for hit in response:
	print(hit)


print('\n\nother syntax')
res = es.search(index="sites3", body=
	{ "query": 
		{"match": 
			{"html": "ouderen"}
		}
	})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
	print(hit['_source']['url'])