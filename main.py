from sanic import Sanic
from sanic.log import log
from model import Person, db
from sanic_crud import generate_crud

# db.create_tables([Person])

app = Sanic(__name__)

app.log = log
generate_crud(app, [Person])
app.go_fast(host='0.0.0.0', port=8000, debug=True)