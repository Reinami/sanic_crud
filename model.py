from peewee import CharField, DateTimeField
from peewee import MySQLDatabase, Model
import datetime
import os
from sanic_crud import CrudConfig, ResponseMessages

db = MySQLDatabase(
    os.environ['MYSQL_DB'],
    host='database',
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASS'],
    )

config = CrudConfig
response_messages = ResponseMessages
response_messages.ErrorTypeDatetime = "I am a custom message: {}"
config.response_messages = response_messages

class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    crud_config = config

    name = CharField()
    email = CharField()
    create_datetime = DateTimeField(default=datetime.datetime.now, null=True)
