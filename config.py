
#
# Mongo Settings
#
MONGODB_CONNECTION = "mongodb://127.0.0.1:27017"
# If you have a replica-set, your config might look a bit like this
# MONGODB_CONNECTION = "mongodb://1.2.3.4:27017,2.3.4.5:27017,4.5.6.7:27017"
MONGO_DATABASE = "google_translation_cache"
MONGO_TRANSLATE_COLLECTION = "translate"

#
# Google API Key
#
GOOGLE_API_KEY = ""

#
# General settings
#
LOG_FILE = "/var/log/google_translate_cache.log"
# number of chars of translation to log in output
LOG_N_CHARS = 100
