from sanic.views import HTTPMethodView
from sanic.response import json
from sanic.log import log


class BaseResource(HTTPMethodView):
    model = None

    def validate_request(self, request):
        log.error(self.model._meta.db_table)

    @staticmethod
    def response_json(data=None, status_code=None, message=None, page=None, total_pages=None):
        response_data = {
            'data': data,
            'status_code': status_code,
            'message': message
        }

        if page:
            response_data['page'] = page
        if total_pages:
            response_data['total_pages'] = total_pages

        return json(response_data, status=status_code)

    def get_model(self, primary_key):
        try:
            pk_field = self.model.shortcuts.primary_key
            return self.model.get(getattr(self.model, pk_field) == primary_key)
        except self.model.DoesNotExist:
            return {}
