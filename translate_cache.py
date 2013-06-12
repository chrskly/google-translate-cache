#!/usr/bin/python

'''
  This is a drop-in cache for the Google Translate API. It uses mongo for
  backend storage and a very simple web.py script.

  Keys
    q = q      : The source string to translate.
    s = source : The source from which to translate.
    t = target : The target language to which to translate.
    r = result : The translated output, in the form:
                 { "data": { "translations": [ { "translatedText": "What eva" } ] } }
'''

import web
import urllib
import urllib2
import datetime
import logging
import simplejson as json
from pymongo import Connection
from config import *

GOOGLE_API_URL = "https://www.googleapis.com/language/translate/v2"

urls = (
  '/translate', 'translate',
  '/test', 'test',
)

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(message)s")

app = web.application(urls, globals())

mongo_connection = Connection(MONGODB_CONNECTION)
database = mongo_connection[MONGO_DATABASE]
translate_collection = database[MONGO_TRANSLATE_COLLECTION]

# make sure we have our indices set up
translate_collection.ensure_index([("q", 1), ("source", 1), ("target", 1)])

class translate:

    def GET(self):
        '''
        params:
          key = Google API Key
          q = The string you want to translate
          source = Source language
          target = Target language
        '''
        start_time = datetime.datetime.now()
        data = web.input()
        key = data['key']
        q = data['q'].lower()
        source = data['source']
        target = data['target']
        global coll
        cached_translation = translate_collection.find_one( { "q" : q, "source" : source, "target": target } )
        if not cached_translation:
            # Don't have this translation in the cache, go fetch it
            url = "%s?%s" % (GOOGLE_API_URL, urllib.urlencode({ "key" : key, "q" : q, "source" : source, "target" : target}))
            result = urllib2.urlopen(url).read()
            json_result = json.loads(result)
            cache_item = { "q" : q, "source" : source, "target" : target, "result" : json_result }
            translate_collection.insert(cache_item)
            end_time = datetime.datetime.now()
            duration = end_time - start_time
            logging.info("%s [%s] miss %s > %s \"%s\"" % (duration.total_seconds(), end_time, source, target, json_result['data']['translations'][0]['translatedText'][:LOG_N_CHARS]))
            return result
        else:
            # Have a copy of this translation in the cache, spit it out
            end_time = datetime.datetime.now()
            duration = end_time - start_time
            translated_text = cached_translation['result']['data']['translations'][0]['translatedText']
            json_result = json.dumps(cached_translation['result'])
            logging.info("%s [%s] hit %s > %s \"%s\"" % (duration.total_seconds(), end_time, source, target, translated_text[:LOG_N_CHARS]))
            return json_result

class test:
    def GET(self):
        ''' Test mongo connection and exit '''
        return translate_collection.count()

         

if __name__ == "__main__":
    app.run()
