import mongoengine

alias_core = 'core'
db = 'snake_db'


def global_setup():
    mongoengine.register_connection(
        alias=alias_core,
        name=db,
    )
