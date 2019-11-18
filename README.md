# U-Flix
Playing around with crawling and making a search engine for some public Municipality of Utrecht websites and data

To play:
* Install Elastic, /bin/elastic.bat (windows)
* Build Elastic index using the stuff in Elastic folder
* Can inspect index using kibana, /bin/kibana.bat (windows)
* Install Django, python manage.py runserver
* Disable the browser security feature to disable CORS
* Open the /interface. Switch search engines in the URL using g (google custom search; default), poc (this elastic one), oris (different dataset)
* Find out and fix what lines I hardcoded because I was very very lazy

Some TODO's:
* setup the google custom search with the same domains
* !weblogging
* deduplication of results
* link to searchlogger firefox extension from a while ago
