import csv
import database

from pymongo import MongoClient

db_config = database.get_mongo_config()

client = MongoClient(db_config['host'], db_config['port'])

db = client[db_config['database']]

collection_name = db_config['collection_name']

if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)

collection = db[collection_name]

# TODO: Create indexes

collection.delete_many({})

try:

    with open('dataset_estudantes.csv', encoding='utf-8') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter=',')

        rows_counter = 0

        for row in csv_reader:

            if row['idade']:
                row['idade'] = int(float(row['idade']))

            if row['ra']:
                row['ra'] = int(float(row['ra']))

            collection.insert_one(row)

            rows_counter += 1

        print('Inserted ' + str(rows_counter) + ' rows')


except FileNotFoundError:

    print('Arquivo não encontrado: crie um arquivo de importação .csv no mesmo diretório deste arquivo')