# Custom Routes

By default, routes for models are defined as `/{tablename}`. You may wish to customzie this route in some cases.
You can do this by adding a `route_url` variable in the model class definition. Keep in mind that if you have
duplicate route definitions you will get an exception from Sanic.

For example, if you want to prepend your url with `/api` you can do this

  ```python
  from sanic_crud import CrudConfig
  from peewee import CharField, DateTimeField, SqliteDatabase, Model
  import datetime
  
  db = SqliteDatabase('my_app.db')
  config = CrudConfig
  config.COLLECTION_MAX_RESULTS_PER_PAGE = 200
    
  class BaseModel(Model):
      class Meta:
            database = db
    
  class Person(BaseModel):
      route_url = '/api/person'
  
      name = CharField()
      email = CharField()
      create_datetime = DateTimeField(default=datetime.datetime.now, null=True)
  
  ```
  
This will now allow access to the Person model from `/api/person`
