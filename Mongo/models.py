from mongoengine import *

connect(host="mongodb://localhost:27017/hw8")


class Authors(Document):
    fullname = StringField(required=True)
    born_date = StringField(max_length=100)
    born_location = StringField(max_length=150)
    description = StringField()


class Qoutes(Document):
    tags = ListField(StringField(max_length=30))
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {"allow_inheritance": True}
