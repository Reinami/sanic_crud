import pytest

from sanic.utils import sanic_endpoint_test
from tests.base_test_app import app


# ------------------------------------------------------------ #
#  GET
# ------------------------------------------------------------ #

# Tests getting a single resource
def test_get_single_resource():
    request, response = sanic_endpoint_test(app, uri='/person')
    print(response.text)

    assert False

# ------------------------------------------------------------ #
#  POST
# ------------------------------------------------------------ #

# Tests creating a new record
def test_create_new_record():
    payload = '{"name":"Sanic the Hedgehog", "email": "gottagofeast@fast.com"}'
    headers = {'content-type': 'application/json'}

    request, response = sanic_endpoint_test(app, uri='/person', data=payload, headers=headers, method='post')

    print(response.text)