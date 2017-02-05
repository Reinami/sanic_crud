from sanic.utils import sanic_endpoint_test
import json


# ------------------------------------------------------------ #
#  GET
# ------------------------------------------------------------ #

def test_get_non_existant_record(app):
    request, response = sanic_endpoint_test(app, uri='/person/404', method='get')
    expected_response = {'data': {},
                         'status_code': 404,
                         'message': "Resource with id '404' does not exist"}

    assert json.loads(response.text) == expected_response


# ------------------------------------------------------------ #
#  POST
# ------------------------------------------------------------ #

def test_post_invalid_json(app):
    payload = '{"name": invalid}'
    headers = {'content-type': 'application/json'}
    request, response = sanic_endpoint_test(app, data=payload, headers=headers, uri='/person', method='post')
    expected_response = {'data': None,
                         'status_code': 400,
                         'message': 'Invalid JSON input'}

    assert json.loads(response.text) == expected_response


def test_post_invalid_field(app):
    payload = {'name': 'Knackles the Echidna', 'email': 'gottapunchfeast@punch.com', 'job': 1, 'yee': 1}
    headers = {'content-type': 'application/json'}
    request, response = sanic_endpoint_test(app, data=json.dumps(payload), headers=headers, uri='/person', method='post')
    expected_response = {'data': None,
                         'status_code': 400,
                         'message': "Field: 'yee' does not exist choices are ['email', 'job', 'name']"}

    assert json.loads(response.text) == expected_response


def test_post_missing_required_field(app):
    payload = {'email': 'gottapunchfeast@punch.com', 'job': 1}
    headers = {'content-type': 'application/json'}
    request, response = sanic_endpoint_test(app, data=json.dumps(payload), headers=headers, uri='/person', method='post')
    expected_response = {'data': None,
                         'status_code': 400,
                         'message': "Field: 'name' cannot be null, required fields are: ['email', 'name']"}

    assert json.loads(response.text) == expected_response


def test_post_int_out_of_range(app):
    payload = {'name': 'Dictator', 'description': 'Ruler of the world', 'base_pay': 3000000000}
    headers = {'content-type': 'application/json'}
    request, response = sanic_endpoint_test(app, data=json.dumps(payload), headers=headers, uri='/job', method='post')
    expected_response = {'data': None,
                         'status_code': 400,
                         'message': "Invalid range for field 'base_pay', must be between -2147483647 and 2147483647"}

    assert json.loads(response.text) == expected_response


# ------------------------------------------------------------ #
#  PUT
# ------------------------------------------------------------ #

def test_put_non_existant_record(app):
    payload = {'email': 'knacklessucks@fast.com'}
    headers = {'content-type': 'application/json'}
    request, response = sanic_endpoint_test(app, data=json.dumps(payload), headers=headers, uri='/person/404', method='put')
    expected_response = {'data': {},
                         'status_code': 404,
                         'message': "Resource with id '404' does not exist"}

    assert json.loads(response.text) == expected_response


def test_put_invalid_json(app):
    payload = '{"name": invalid}'
    headers = {'content-type': 'application/json'}
    request, response = sanic_endpoint_test(app, data=payload, headers=headers, uri='/person/1', method='put')
    expected_response = {'data': None,
                         'status_code': 400,
                         'message': 'Invalid JSON input'}

    assert json.loads(response.text) == expected_response


def test_put_invalid_field(app):
    payload = {'name': 'Knackles the Echidna', 'email': 'gottapunchfeast@punch.com', 'job': 1, 'yee': 1}
    headers = {'content-type': 'application/json'}
    request, response = sanic_endpoint_test(app, data=json.dumps(payload), headers=headers, uri='/person/1', method='put')
    expected_response = {'data': None,
                         'status_code': 400,
                         'message': "Field: 'yee' does not exist choices are ['email', 'job', 'name']"}

    assert json.loads(response.text) == expected_response

def test_put_int_out_of_range(app):
    payload = {'base_pay': 3000000000}
    headers = {'content-type': 'application/json'}
    request, response = sanic_endpoint_test(app, data=json.dumps(payload), headers=headers, uri='/job/1', method='put')
    expected_response = {'data': None,
                         'status_code': 400,
                         'message': "Invalid range for field 'base_pay', must be between -2147483647 and 2147483647"}

    assert json.loads(response.text) == expected_response


# ------------------------------------------------------------ #
#  DELETE
# ------------------------------------------------------------ #

def test_delete_non_existant_record(app):
    request, response = sanic_endpoint_test(app, uri='/person/2', method='delete')
    expected_response = {'data': {},
                         'status_code': 404,
                         'message': "Resource with id '2' does not exist"}

    assert json.loads(response.text) == expected_response

def test_put_invalid_json(app):
    request, response = sanic_endpoint_test(app, uri='/job/2', method='delete')
    expected_response = {'data': {},
                         'status_code': 404,
                         'message': "Resource with id '2' does not exist"}

    assert json.loads(response.text) == expected_response