import mongoengine

from src import config

alias_core = config.mongo_alias
db = config.mongo_db
username = config.mongo_username
password = config.mongo_password

host = f'mongodb+srv://{username}:{password}@testcluster-9feub.azure.mongodb.net/{db}?retryWrites=true&w=majority'


def global_setup():
    mongoengine.register_connection(
        alias=alias_core,
        db=db,
        host=host

    )
