from peewee import CharField, DateTimeField
from peewee import MySQLDatabase, Model
import os

db = MySQLDatabase(
    os.environ['MYSQL_DB'],
    host='database',
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASS'],
    )


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = CharField()
    email = CharField()
    create_datetime = DateTimeField(null=True)
