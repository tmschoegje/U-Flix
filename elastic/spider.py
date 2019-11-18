#Hacky approach to crawling the sites

# Installation: pip install Scrapy
# Running: scrapy runspider spider.py -o sites.json

# Code based on copied crawler example from https://docs.scrapy.org/en/latest/intro/tutorial.html

# Todo: make some use of the meta-data in sites like the volksgezondheidsmonitor
# <meta name="Keywords" content="bevolking Utrecht inwoners Utrechters leeftijd, ouderen, pubers, studenten">
#		<meta name="Description" content="Utrecht heeft veel jonge inwoners. Hoe is de leeftijdsopbouw in de stad?">
# Q: Is this approach according to a metadata standard that describes how to prepare html pages? Would be good for re-using info

# Note: Elastic Site Search is misschien een realistisch alternatief - lijkt vrij makkelijk te onderhouden

#TODO met elastic sites.json indexeren. 
#parse json. 
#Search erop runnen.
#Recommend by url

import scrapy
from time import sleep

#HTML stripper first
#note: now using a different stripping method

from html.parser import HTMLParser

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


#Our spider describes how we crawl
class SitesSpider(scrapy.Spider):
	#Name of the spider
	name = 'sites'
	#Add the homepage of sites we want to crawl here
	start_urls = [
		'http://utrecht-monitor.nl/',   #volksgezondheidsmonitor.nl
	]
	#If we allow other domains, we'lls tart indexing twitter etc through the links
	allowed_domains = ['utrecht-monitor.nl']

	# Function that describes how every URL found will be parsed
	def parse(self, response):
		# Parse the results using css selectors
		# Naive approach: using the first result
		# Ignores pdf's for example, because those should be parsed
		# differently
		yield {
			'url': response.url,
			'title': response.css('title::text').get(),
			'keywords': response.css('meta[keywords]').get(),
			'html': response.css('html').get()
		}
	
		# Sample Code
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
		if next_page is not None:
			#For each url found, parse it
			for page in next_page:
				next = response.urljoin(page)
				yield response.follow(next, self.parse)