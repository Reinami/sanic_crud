from peewee import CharField, DateTimeField, SqliteDatabase, Model
import datetime
from sanic_crud import CrudConfig


db = SqliteDatabase('my_app.db')


class BaseModel(Model):
    class Meta:
        database = db

config = CrudConfig()
config.COLLECTION_MAX_RESULTS_PER_PAGE = 500


class Person(BaseModel):
    crud_config = config

    name = CharField()
    email = CharField()
    create_datetime = DateTimeField(default=datetime.datetime.now, null=True)
