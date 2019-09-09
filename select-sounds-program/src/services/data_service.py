import os
import subprocess
from typing import List, Dict

from src import config
from data.owners import Owner
from data.records import Record

DIR_PATH = os.path.abspath(os.path.dirname(__file__))


def create_account(name: str, email: str) -> Owner:
    owner = Owner()
    owner.name = name
    owner.email = email

    owner.save()

    return owner


def find_account_by_email(email: str) -> Owner:
    owner = Owner.objects(email=email).first()
    return owner


def add_record(record_data: Dict, cost: float = None) -> Record:
    record = Record()

    record.name = record_data['name']
    record.artist = record_data['artist']
    record.label = record_data['label']
    record.country = record_data['country']
    record.release_date = record_data['release-date']
    record.genre = record_data['genre']
    record.format = record_data['format']
    record.size = record_data['size']
    record.speed = record_data['speed']
    record.tracklist = record_data['tracklist']
    record.lowest_price = record_data['lowest-price']
    record.median_price = record_data['median-price']
    record.highest_price = record_data['highest-price']

    if cost:
        record.cost = cost

    record.save()

    return record


def check_existing_records(name: str, artist: str) -> List[Record]:
    query = Record.objects(name=name, artist=artist)
    return query


def export_record_data(fields: List):
    path_to_export_command = config.ROOT_DIR + '/export_record_data.sh'

    username = config.mongo_username
    password = config.mongo_password
    database = config.mongo_db

    if fields:
        command_fields = ','.join(fields)
        file_name = '_'.join([f.replace('_', '-') for f in fields]) + '_records.csv'
        print(file_name)
    else:
        command_fields = 'name,artist,label,country,release_date,speed,tracklist'
        file_name = 'records.csv'

    command = ['sh', f'{path_to_export_command}', username, password, database, command_fields, file_name]

    export_record_data_command = subprocess.run(command, stderr=subprocess.PIPE)
    return file_name, export_record_data_command.returncode, export_record_data_command.stderr


# def get_records_data_file() -> str:
#     if os.path.exists(config.ROOT_DIR + '/data/records.csv'):
#         return 'src/data/records.csv'


def convert_letters_to_fields(field_keys: str):
    field_dict = {
        'n': 'name',
        'a': 'artist',
        'l': 'label',
        'c': 'country',
        'r': 'release_date',
        'g': 'genre',
        'f': 'format',
        's': 'size',
        'e': 'speed',
        'o': 'lowest_price',
        'm': 'median_price',
        'h': 'highest_price'
    }
    fields = []
    for f in field_keys:
        # if f in field_dict.values():
        #     fields.append(f)
        if f in field_dict.keys():
            if field_dict[f] not in fields:
                fields.append(field_dict[f])

    return fields
