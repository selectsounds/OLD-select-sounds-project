import mongoengine
import dns

alias_core = 'select-sounds'
db = 'selectsoundsdb'


# Connection-string: 'mongodb+srv://SelectSounds:beatsbyer@testcluster-9feub.azure.mongodb.net/test?retryWrites=true&w=majority'

def global_setup():
    mongoengine.register_connection(
        alias=alias_core,
        db=db,
        # username='SelectSounds',
        # password='beatsbyer',
        host='mongodb+srv://SelectSounds:beatsbyer@testcluster-9feub.azure.mongodb.net/selectsoundsdb?retryWrites=true&w=majority'

    )
