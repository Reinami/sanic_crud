from sanic.utils import sanic_endpoint_test
import json


def test_custom_message(app):
    request, response = sanic_endpoint_test(app, uri='/person/1', method='get')
    expected_messages = 'Cool Brah'

    assert json.loads(response.text).get('message') == expected_messages


def test_custom_pagination(app):
    request, response = sanic_endpoint_test(app, uri='/job', method='get')
    page_one = json.loads(response.text)
    request, response = sanic_endpoint_test(app, uri='/job?page=2', method='get')
    page_two = json.loads(response.text)

    assert len(page_one.get('data')) == 1
    assert page_one.get('total_pages') == 2

    assert len(page_two.get('data')) == 1
    assert page_two.get('total_pages') == 2
    assert page_two.get('page') == 2
