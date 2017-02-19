from sanic.utils import sanic_endpoint_test
import json


# ------------------------------------------------------------ #
#  GET
# ------------------------------------------------------------ #

def test_get_collection_resource(app):
    request, response = sanic_endpoint_test(app, uri='/job', method='get')
    expected_response = {'data': [
                             {
                                 'id': 1,
                                 'name': 'Space garbage man',
                                 'description': 'Collects garbage in space',
                                 'base_pay': 15
                             }
                         ],
                         'status_code': 200,
                         'message': 'OK',
                         'page': 1,
                         'total_pages': 1}

    assert json.loads(response.text) == expected_response


def test_get_single_resource(app):
    request, response = sanic_endpoint_test(app, uri='/person/1', method='get')
    expected_response = {'data': {
        'id': 1,
        'name': 'Sanic the Hedgehog',
        'job': 1,
        'email': 'gottagofeast@fast.com'},
        'status_code': 200,
        'message': "OK"}

    assert json.loads(response.text) == expected_response


def test_get_foreign_keys(app):
    request, response = sanic_endpoint_test(app, uri='/person/1?foreign_keys=true', method='get')
    expected_response = {'data': {
        'id': 1,
        'name': 'Sanic the Hedgehog',
        'job': {
            'id': 1,
            'name': 'Space garbage man',
            'description': 'Collects garbage in space',
            'base_pay': 15
        },
        'email': 'gottagofeast@fast.com'},
        'status_code': 200,
        'message': "OK"
    }

    assert expected_response == json.loads(response.text)


def test_get_backrefs(app):
    request, response = sanic_endpoint_test(app, uri='/job/1?backrefs=true', method='get')
    expected_repsonse = {
        'data': {
            'id': 1,
            'name': "Space garbage man",
            'description': "Collects garbage in space",
            'base_pay': 15,
            'person_job': [{
                'id': 1,
                'name': "Sanic the Hedgehog",
                'email': "gottagofeast@fast.com"
            }]
        },
        'status_code': 200,
        'message': "OK"
        }

    assert expected_repsonse == json.loads(response.text)


# ------------------------------------------------------------ #
#  POST
# ------------------------------------------------------------ #

def test_create_new_record(app):
    payload = {'name': 'Knackles the Echidna', 'email': 'gottapunchfeast@punch.com', 'job': 1}
    headers = {'content-type': 'application/json'}
    request, response = sanic_endpoint_test(app,
                                            uri='/person',
                                            data=json.dumps(payload),
                                            headers=headers,
                                            method='post')
    expected_response = {'data': {
                             'id': 2,
                             'name': 'Knackles the Echidna',
                             'job': {
                                 'id': 1,
                                 'name': 'Space garbage man',
                                 'description': 'Collects garbage in space',
                                 'base_pay': 15
                             },
                             'email': 'gottapunchfeast@punch.com'},
                         'status_code': 200,
                         'message': "Resource with id '2' was created!"}

    assert json.loads(response.text) == expected_response


# ------------------------------------------------------------ #
#  PUT
# ------------------------------------------------------------ #

def test_update_record(app):
    payload = {'email': 'knacklessucks@fast.com'}
    headers = {'content-type': 'application/json'}
    request, response = sanic_endpoint_test(app,
                                            uri='/person/1',
                                            data=json.dumps(payload),
                                            headers=headers,
                                            method='put')

    expected_response = {'data': {
                             'id': 1, 'name': 'Sanic the Hedgehog',
                             'job': {
                                 'id': 1,
                                 'name': 'Space garbage man',
                                 'description': 'Collects garbage in space',
                                 'base_pay': 15
                             },
                             'email': 'knacklessucks@fast.com'},
                         'status_code': 200,
                         'message': 'OK'}

    assert json.loads(response.text) == expected_response


# ------------------------------------------------------------ #
#  DELETE
# ------------------------------------------------------------ #

def test_delete_record(app):
    request, response = sanic_endpoint_test(app, uri='/person/1', method='delete')
    expected_response = {'data': None,
                         'status_code': 200,
                         'message': "Resource with id '1' was deleted!"}

    assert json.loads(response.text) == expected_response
