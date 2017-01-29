# Custom Configuration

There are several values that are configured by default in sanic_crud,
such as how many entries per page there can be for a collection resource. These values are actually configurable
per model through a special crud_config attribute

For example, if you want to set the maximum pages to 200 instead of 100, you could create your model like this

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
      crud_config = config
  
      name = CharField()
      email = CharField()
      create_datetime = DateTimeField(default=datetime.datetime.now, null=True)
  
  ```
  
The default configuration values can be found in the sanic_crud/crud_config.py file

This will update the config for this model when you use it. You can also do this to change the messages that you see as well

**Next** [Custom Response Messages](custom_response_messages.md)
