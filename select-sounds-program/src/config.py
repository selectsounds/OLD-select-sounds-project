import os
import configparser

ROOT_DIR: str = os.path.abspath(os.path.dirname(__file__))

mongo_alias: str
mongo_db: str
mongo_username: str
mongo_password: str


def setup_config():
    config_path = f'{ROOT_DIR}/config.ini'

    if not os.path.exists(config_path):
        raise FileNotFoundError('No config.ini file found. Exiting...')

    config = configparser.ConfigParser()

    config.read(config_path)

    global mongo_alias
    mongo_alias = config['DATABASE']['mongo_alias']

    global mongo_db
    mongo_db = config['DATABASE']['mongo_db']

    global mongo_username
    mongo_username = config['DATABASE']['mongo_username']

    global mongo_password
    mongo_password = config['DATABASE']['mongo_password']


setup_config()
