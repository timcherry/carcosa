from mongoengine import *
from carcosa.settings import DBNAME

connect(DBNAME)


from django.db import models
from datetime import datetime

# Create your models here.
class Post(Document):
    company = StringField(max_length=128)
    position = StringField(max_length=128)
    full_comment = StringField()
    hidden_comment = StringField()
    sub_date = DateTimeField(default=datetime.utcnow)