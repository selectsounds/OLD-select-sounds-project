import os

import configparser

mongo_alias: str = None
mongo_db: str = None
mongo_username: str = None
mongo_password: str = None


def setup_config():
    cwd = os.path.abspath(os.path.dirname(__file__))
    config_path = f'{"/".join(cwd.split("/")[:-2])}/config.ini'

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
