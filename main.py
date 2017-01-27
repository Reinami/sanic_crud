from sanic import Sanic
from model import Person, db
from sanic_crud import BaseResource, BaseCollectionResource

class PersonResource(BaseResource):
    model = Person

class PersonCollectionResource(BaseCollectionResource):
    model = Person

# db.create_tables([Person])

app = Sanic(__name__)

app.add_route(PersonResource.as_view(), '/person/<id:int>')
app.add_route(PersonCollectionResource.as_view(), '/person')

app.go_fast(host='0.0.0.0', port=8000, debug=True)
