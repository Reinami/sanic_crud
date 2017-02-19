from peewee import SqliteDatabase, Model, CharField, DateTimeField, IntegerField, ForeignKeyField
from sanic import Sanic
from sanic.log import log
import datetime

from sanic_crud import generate_crud

db = SqliteDatabase('dev_data.db')


class BaseModel(Model):
    class Meta:
        database = db


class Job(BaseModel):
    route_url = '/yee/yee/s'
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
app.go_fast(host='0.0.0.0', port=8000, debug=True)
