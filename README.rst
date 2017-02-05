sanic_crud 
=================================

|Build Status|   |PyPI|   |PyPI version|

sanic_crud is a REST API framework for creating a CRUD (Create/Retrieve/Update/Delete) API using `Sanic <https://github.com/channelcat/sanic>`_ and `PeeWee <http://docs.peewee-orm.com/en/latest/>`_
You can use sanic_crud to automatically create an API from your PeeWee models, see how it works in the `Documentation <docs/using_a_sanic_crud_api.md>`_
Contributions to the repository are welcome!

Example
----------

.. code:: python

    from peewee import CharField, DateTimeField, SqliteDatabase, Model
    import datetime
    from sanic import Sanic
    from sanic_crud import generate_crud
    
    db = SqliteDatabase('my_app.db')
    
    class BaseModel(Model):
        class Meta:
            database = db
    
    class Person(BaseModel):
        name = CharField()
        email = CharField()
        create_datetime = DateTimeField(default=datetime.datetime.now, null=True)
    
    db.create_tables([Person])
    
    app = Sanic(__name__)
    generate_crud(app, [Person])
    app.run(host="0.0.0.0", port=8000, debug=True)

Installation
------------

-  `python -m pip install sanic-crud`

Documentation
-------------

Documentation can be found in the ``docs`` directory.

.. |Build Status| image:: https://travis-ci.org/Typhon66/sanic_crud.svg?branch=master
    :target: https://travis-ci.org/Typhon66/sanic_crud
.. |PyPI| image:: https://badge.fury.io/py/sanic-crud.svg
    :target: https://badge.fury.io/py/sanic-crud
.. |PyPI version| image:: https://img.shields.io/pypi/pyversions/sanic-crud.svg
   :target: https://pypi.python.org/pypi/sanic-crud


TODO
----

* `Add sanic_openapi/swagger support <https://github.com/Typhon66/sanic_crud/issues/11>`_
* `Add support for custom routes per model <https://github.com/Typhon66/sanic_crud/issues/7>`_
* `Make int/string length validation better <https://github.com/Typhon66/sanic_crud/issues/5>`_
