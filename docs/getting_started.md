# Getting Started

Make sure you have both [pip](https://pip.pypa.io/en/stable/installing/) and at
least version 3.5 of Python before starting. sanic_crud requires [Sanic.](https://github.com/channelcat/sanic)
Additionally see [peewee documentation](http://docs.peewee-orm.com/en/latest/) as well.

1. Install sanic_crud: `python3 -m pip install sanic_crud`
2. Create a file called `main.py` with the following code:
    
  ```python
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
  ```
  
3. Run the server: `python3 main.py`
4. Open the address `http://0.0.0.0:8000/person` in your browser,
   you should see an response: 
   
   ```json
   {
    "data": [],
    "status_code": 200,
    "message": "OK",
    "page": 1
   }
   ```

You now have a working sanic_crud server!

**Next:** [Using the service](using_a_sanic_crud_api.md)
