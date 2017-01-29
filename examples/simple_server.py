from sanic import Sanic
from sanic_crud import generate_crud
from .model import db, Person


db.create_tables([Person])

app = Sanic(__name__)
generate_crud(app, [Person])
app.run(host="0.0.0.0", port=8000, debug=True)
