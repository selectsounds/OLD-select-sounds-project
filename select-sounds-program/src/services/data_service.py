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


def export_record_data():
    path_to_export_command = config.ROOT_DIR + '/export_record_data.sh'

    export_record_data_command = subprocess.run(['sh', f'{path_to_export_command}'], stderr=subprocess.PIPE)
    return export_record_data_command.returncode, export_record_data_command.stderr


def get_records_data_file() -> str:
    if os.path.exists(config.ROOT_DIR + '/data/records.csv'):
        return 'src/data/records.csv'
