from decouple import config

config = {
    'host': config('MONGO_DB_HOST', default='localhost'),
    'port': config('MONGO_DB_PORT', default=27017, cast=int),
    'database': config('MONGO_DB_DATABASE', default='laura_challenge'),
    'collection_name': config('MONGO_DB_COLLECTION', default='estudantes')
}


def get_mongo_config():
    return config


def get_mongo_uri():
    return 'mongodb://' + config['host'] + ':' + str(config['port']) + '/' + config['database']
