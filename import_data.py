import csv

from database import mongo_config
from pymongo import MongoClient

db_config = mongo_config()

client = MongoClient(db_config['host'], db_config['port'])

db = client[db_config['database']]

collection_name = db_config['collection_name']

if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)

collection = db[collection_name]

collection.create_index([('ra', 1)])
collection.create_index([('cursos.campus', 1)])

collection.delete_many({})


def get_course_dict(row={}):

    return {
        'campus': row['campus'].strip() if row['campus'] else None,
        'municipio': row['municipio'].strip() if row['municipio'] else None,
        'curso': row['curso'].strip() if row['curso'] else None,
        'modalidade': row['modalidade'].strip() if row['modalidade'] else None,
        'nivel_do_curso': row['nivel_do_curso'].strip() if row['nivel_do_curso'] else None,
        'data_inicio': row['data_inicio']
    }


try:

    with open('dataset_estudantes.csv', encoding='utf-8') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter=',')

        row_counter = 0

        to_insert = []

        ra_and_index = {}

        for row in csv_reader:

            if row['ra'] in ra_and_index:

                index = ra_and_index.get(row['ra'])

                to_insert[index]['cursos'].append(get_course_dict(row))

                continue

            elif row['ra']:

                ra_and_index[row['ra']] = row_counter

            if row['idade_ate_31_12_2016']:

                row['idade_ate_31_12_2016'] = int(float(row['idade_ate_31_12_2016']))

            if row['ra']:

                row['ra'] = int(float(row['ra']))

            to_insert.append({
                'nome': row['nome'].strip() if row['nome'] else None,
                'idade_ate_31_12_2016': row['idade_ate_31_12_2016'],
                'ra': row['ra'],
                'cursos': [get_course_dict(row)]
            })

            row_counter += 1

        ids = collection.insert_many(to_insert).inserted_ids

        print('Inserted ' + str(len(ids)) + ' students')


except FileNotFoundError:

    print('Arquivo não encontrado: crie um arquivo de importação dataset_estudantes.csv no mesmo diretório deste arquivo')
