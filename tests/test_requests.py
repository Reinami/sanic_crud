import pytest

from sanic.utils import sanic_endpoint_test
import json


@pytest.fixture
def app(request):
    from peewee import SqliteDatabase, Model, CharField, DateTimeField, IntegerField, ForeignKeyField
    from sanic import Sanic
    from sanic.log import log
    import os
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
    db.create_tables([Person, Job])

    job = Job(name="Space garbage man", description="Collects garbage in space", base_pay=15)
    person = Person(name="Sanic the Hedgehog", email="gottagofeast@fast.com", job=1)

    job.save()
    person.save()

    test_app = Sanic(__name__)

    test_app.log = log
    generate_crud(test_app, [Person, Job])

    def teardown():
        os.remove('tests/test.db')

    request.addfinalizer(teardown)
    return test_app


# ------------------------------------------------------------ #
#  GET
# ------------------------------------------------------------ #

# Tests getting a single resource
def test_get_single_resource(app):
    request, response = sanic_endpoint_test(app, uri='/job')
    response_meta = json.loads(response.text)
    response_data = response_meta.get('data')
    print(response_data)

    # Test response
    assert response_meta.get('status_code') == 200
    assert response_meta.get('page') == 1
    assert response_meta.get('total_pages') == 1
    assert response_meta.get('message') == 'OK'

    # Test data
    assert len(response_data) == 1
    assert response_data[0].get('id') == 1
    assert response_data[0].get('name') == "Space garbage man"
    assert response_data[0].get('description') == "Collects garbage in space"
    assert response_data[0].get('base_pay') == 15

# ------------------------------------------------------------ #
#  POST
# ------------------------------------------------------------ #

# Tests creating a new record
# def test_create_new_record():
#     payload = '{"name":"Sanic the Hedgehog", "email": "gottagofeast@fast.com"}'
#     headers = {'content-type': 'application/json'}
#
#     request, response = sanic_endpoint_test(app, uri='/person', data=payload, headers=headers, method='post')
#
#     print(response.text)