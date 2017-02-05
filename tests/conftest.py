import pytest


# Setup the data for each test
@pytest.fixture(autouse=True)
def app(request):
    from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField
    from sanic import Sanic
    from sanic.log import log

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
        job = ForeignKeyField(Job, related_name='person_job', null=True)
        email = CharField()

    db.create_tables([Person, Job])
    job = Job(name='Space garbage man', description='Collects garbage in space', base_pay=15)
    person = Person(name='Sanic the Hedgehog', email='gottagofeast@fast.com', job=1)
    job.save()
    person.save()

    test_app = Sanic(__name__)

    test_app.log = log
    generate_crud(test_app, [Person, Job])

    def final():
        db.drop_tables([Person, Job])

    request.addfinalizer(final)
    return test_app
