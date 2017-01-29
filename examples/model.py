from peewee import CharField, DateTimeField, SqliteDatabase, Model
import datetime


db = SqliteDatabase('my_app.db')


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = CharField()
    email = CharField()
    create_datetime = DateTimeField(default=datetime.datetime.now, null=True)
