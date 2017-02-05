from peewee import SqliteDatabase, Model, CharField, DateTimeField, IntegerField, ForeignKeyField
from sanic import Sanic
from sanic.log import log
import datetime

from sanic_crud import generate_crud


db = SqliteDatabase('tests/test.db')


class BaseModel(Model):
    class Meta:
        database = db


class Job(BaseModel):
    name = CharField()
    description = CharField()
    base_pay = IntegerField()


class Person(BaseModel):
    name = CharField()
    job = ForeignKeyField(Job, related_name="person_job", null=True)
    email = CharField()
    create_datetime = DateTimeField(default=datetime.datetime.now, null=True)


# if there is an error DB already exists
try:
    db.create_tables([Person, Job])
except Exception:
    pass

app = Sanic(__name__)

app.log = log
generate_crud(app, [Person, Job])
