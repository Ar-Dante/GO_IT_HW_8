from mongoengine import *

connect(host="mongodb://localhost:27017/hw8")


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(max_length=50)
    phone = StringField(max_length=25)
    send = BooleanField(default=False)
    send_method = StringField(max_length=25)
