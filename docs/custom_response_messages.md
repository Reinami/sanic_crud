# Custom Response Messages

Responses by default have a response in them, when the user enters something incorrectly or there is an error
the message is displayed. You can customize these messages on a per model basis by doing the following: 

  ```python
  from peewee import CharField, DateTimeField
  from peewee import MySQLDatabase, Model
  import datetime
  import os
  from sanic_crud import CrudConfig, ResponseMessages
  
  db = MySQLDatabase(
      os.environ['MYSQL_DB'],
      host='database',
      user=os.environ['MYSQL_USER'],
      password=os.environ['MYSQL_PASS'],
      )
  
  config = CrudConfig
  response_messages = ResponseMessages
  response_messages.ErrorTypeDatetime = "I am a custom message: {}"
  config.response_messages = response_messages
  
  class BaseModel(Model):
      class Meta:
          database = db
  
  
  class Person(BaseModel):
      crud_config = config
  
      name = CharField()
      email = CharField()
      create_datetime = DateTimeField(default=datetime.datetime.now, null=True)
  ```
  
This will create a custom message whenever ErrorTypeDatetime is triggered. You can do this for every error message. 
The default error messages can be found in the sanic_crud/crud_config.py file