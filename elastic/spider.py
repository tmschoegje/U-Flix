#Hacky approach to crawling the sites

# Installation: pip install Scrapy
# Running: scrapy runspider spider.py -o sites.json

# Code based on copied crawler example from https://docs.scrapy.org/en/latest/intro/tutorial.html

# Todo: make some use of the meta-data in sites like the volksgezondheidsmonitor
# <meta name="Keywords" content="bevolking Utrecht inwoners Utrechters leeftijd, ouderen, pubers, studenten">
#		<meta name="Description" content="Utrecht heeft veel jonge inwoners. Hoe is de leeftijdsopbouw in de stad?">
# Q: Is this approach according to a metadata standard that describes how to prepare html pages? Would be good for re-using info

# Note: Elastic Site Search is misschien een realistisch alternatief - lijkt vrij makkelijk te onderhouden

import scrapy
from time import sleep
import html2text
import re
from urllib.parse import urlparse

#old HTML stripper code

from html.parser import HTMLParser
import re
import time
from nltk import tokenize

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#testing this html stripper
# https://github.com/Alir3z4/html2text
h = html2text.HTML2Text()
h.ignore_links = True

parsedAllowed = set()

#Our spider describes how we crawl
class SitesSpider(scrapy.Spider):
	#Name of the spider
	name = 'sites'
	#Add the homepage of sites we want to crawl here
	start_urls = [
		'http://utrecht-monitor.nl/',   #volksgezondheidsmonitor.nl
		'http://utrecht.nl/',
		'http://wistudata.nl/',
		'http://volksgezondheidsmonitor.nl/',
		'https://utrecht.jaarverslag-2018.nl/',
		'https://030laadpaal.nl/',
		'http://utrecht2018.mpso.nl/',
		'https://www.integriteitsrapportagegemeenteraadutrecht.nl/',
		'https://www.jeugdengezinutrecht.nl/',
		'http://www.welstandutrecht.nl/',
		'https://www.voorzieningenkaartutrecht.nl/',
		'https://utrecht.dataplatform.nl/',
		'http://ugids.nl',
	]
	#If we allow other domains, we'lls tart indexing twitter etc through the links
	allowed_domains = [
    	'utrecht-monitor.nl',   #volksgezondheidsmonitor.nl
		'utrecht.nl',
		'wistudata.nl',
		'volksgezondheidsmonitor.nl',
		'utrecht.jaarverslag-2018.nl',
		'030laadpaal.nl',
		'utrecht2018.mpso.nl',
		'integriteitsrapportagegemeenteraadutrecht.nl',
		'jeugdengezinutrecht.nl',
		'welstandutrecht.nl',
		'voorzieningenkaartutrecht.nl',
		'utrecht.dataplatform.nl',
		'ugids.nl',
	]

	#parsed with urllib for my own bookkeping of what urls go off these domains
	parsedAllowed = [urlparse(x).netloc for x in allowed_domains]
	#sleep(1)
    
	# Function that describes how every URL found will be parsed
	def parse(self, response):
		# Parse the results using css selectors
		# Naive approach: using the first result
		# Ignores pdf's for example, because those should be parsed
		# differently

		#for stripping html and special chars
		#st = sxtrip_tags(response.css('body').get())
		#body = ''re.sub('\W+',' ', string )#        .join(e for e in st if e.isalnum())

		yield {
			'url': response.url,
			'title': response.css('title::text').get(),
			'keywords': response.css('meta[keywords]').get(),
			'markdownbody': h.handle(response.css('body').get()),#strip_tags(response.css('body').get()).replace("\r",'').replace("\n",'').replace("\t",''),
			'html': response.css('html').get(),
			'urls': set([urlparse(x).netloc for x in response.css('a::attr(href)').getall()]) - parsedAllowed
		}
	
		print(set([urlparse(x).netloc for x in response.css('a::attr(href)').getall()]) - parsedAllowed)# Sample Code
        #for quote in response.css('div.quote'):
        #    yield {
        #        'text': quote.css('span.text::text').get(),
        #        'author': quote.xpath('span/small/text()').get(),
        #    }

		# Now, what page should be parsed next?
		# Current naive approach: just get all hrefs on the page
		#for a in response.css('a'):
		#	yield response.follow(a, callback=self.parse)		
		
		#old code 
		next_page = response.css('a::attr(href)').getall()
		print('WE ZIJN ER')
		print(next_page)
        
		if next_page is not None:
			#For each url found, parse it
			for page in next_page:
				next = response.urljoin(page)
				yield response.follow(next, self.parse)