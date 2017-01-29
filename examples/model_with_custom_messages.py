from peewee import CharField, DateTimeField, SqliteDatabase, Model
import datetime
from sanic_crud import CrudConfig, ResponseMessages


db = SqliteDatabase('my_app.db')


class BaseModel(Model):
    class Meta:
        database = db

config = CrudConfig()
response_messages = ResponseMessages()
response_messages.ErrorDoesNotExist = 'Custom error message here: {}'
config.response_messages = response_messages


class Person(BaseModel):
    crud_config = config

    name = CharField()
    email = CharField()
    create_datetime = DateTimeField(default=datetime.datetime.now, null=True)
