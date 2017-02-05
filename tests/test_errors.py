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

# Make this pass first
# def test_post_invalid_json(app):
#     request, response = sanic_endpoint_test(app, uri='/person', method='post')
#     expected_response = '{"name": invalid json}'
#
#     print(json.loads(response.text))
#
#     assert 0
#     assert json.loads(response.text) == expected_response


# Make this pass first
# def test_post_invalid_field(app):
#     payload = {'name': 'Knackles the Echidna', 'email': 'gottapunchfeast@punch.com', 'job': 1, 'yee': 1}
#     headers = {'content-type': 'application/json'}
#     request, response = sanic_endpoint_test(app, data=json.dumps(payload), headers=headers, uri='/person', method='post')
#
#     print(response.text)
#     assert 0

def test_post_missing_required_field(app):
    payload = {'email': 'gottapunchfeast@punch.com', 'job': 1}
    headers = {'content-type': 'application/json'}
    request, response = sanic_endpoint_test(app, data=json.dumps(payload), headers=headers, uri='/person', method='post')
    expected_response = {'data': None,
                         'status_code': 400,
                         'message': "Field: 'name' cannot be null, required fields are: ['name', 'email']"}

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

# Make this pass first
# def test_put_invalid_json(app):
#     request, response = sanic_endpoint_test(app, uri='/job/1', method='put')
#     expected_response = '{"name": invalid json}'
#
#     print(json.loads(response.text))
#
#     assert 0
#     assert json.loads(response.text) == expected_response

# Make this pass first
# def test_put_invalid_field(app):
#     payload = {'name': 'Knackles the Echidna', 'email': 'gottapunchfeast@punch.com', 'job': 1, 'yee': 1}
#     headers = {'content-type': 'application/json'}
#     request, response = sanic_endpoint_test(app, data=json.dumps(payload), headers=headers, uri='/person/1', method='post')
#
#     print(response.text)
#     assert 0

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

# Make this pass first
# def test_put_invalid_json(app):
#     request, response = sanic_endpoint_test(app, uri='/job/2', method='delete')
#     expected_response = {'data': {},
#                          'status_code': 404,
#                          'message': "Resource with id '2' does not exist"}
#
#     assert json.loads(response.text) == expected_response