import datetime
import mongoengine


class Record(mongoengine.Document):
    date_registered = mongoengine.DateTimeField(default=datetime.datetime.now)

    name = mongoengine.StringField(required=True)
    artist = mongoengine.StringField(required=True)
    label = mongoengine.StringField(required=True)
    country = mongoengine.StringField(required=True)
    release_date = mongoengine.StringField(required=True)
    format = mongoengine.StringField()  # single / LP / EP / Album
    size = mongoengine.StringField()
    speed = mongoengine.StringField()
    tracklist = mongoengine.ListField()
    lowest_price = mongoengine.FloatField(required=True)
    median_price = mongoengine.FloatField(required=True)
    highest_price = mongoengine.FloatField(required=True)
    cost = mongoengine.FloatField(default=1.00)

    meta = {
        'db_alias': 'select-sounds',
        'collection': 'records'
    }

    @property
    def price_difference(self) -> float:
        return self.median_price - self.cost
