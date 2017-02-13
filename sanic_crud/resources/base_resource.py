from sanic.views import HTTPMethodView
from sanic.response import json
from sanic.log import log


class BaseResource(HTTPMethodView):
    model = None

    def validate_request(self, request):
        validations = []
        validations.append(self._validate_primary_key_immutable(request))
        validations.append(self._validate_field_types(request))
        validations.append(self._validate_fields(request))
        validations.append(self._validate_field_length(request))
        validations.append(self._validate_field_size(request))

        for validation in validations:
            if validation is not True:
                return validation

        return True

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

    def get_model(self, pk):
        try:
            pk_field = self.model.shortcuts.primary_key
            return self.model.get(getattr(self.model, pk_field) == pk)
        except self.model.DoesNotExist:
            return {}

    def _validate_primary_key_immutable(self, request):
        if self.model.shortcuts.primary_key in request.json:
            return self.response_json(status_code=400,
                                      message=self.config.response_messages.ErrorPrimaryKeyUpdateInsert)
        else:
            return True

    def _validate_field_types(self, request):
        shortcuts = self.model.shortcuts
        response_messages = self.config.response_messages
        fields = shortcuts.editable_fields
        request_data = request.json

        for key, value in request_data.items():
            expected_type = fields.get(key).db_field

            if expected_type in ['int', 'bool']:
                try:
                    int(value)
                except (ValueError, TypeError):
                    if expected_type == 'int':
                        message = response_messages.ErrorTypeInteger.format(value)
                    else:
                        message = response_messages.ErrorTypeBoolean.format(value)

                    return self.response_json(status_code=400, message=message)

        return True

    def _validate_fields(self, request):
        fields = self.model.shortcuts.editable_fields
        request_data = request.json

        for key in request_data:
            if key not in fields:
                return self.response_json(status_code=400,
                                          message=self.config.response_messages.ErrorInvalidField.format(key, [key for key in fields.keys()]))

        return True

    def _validate_field_length(self, request):
        shortcuts = self.model.shortcuts
        response_messages = self.config.response_messages

        fields = shortcuts.editable_fields
        required_fields = shortcuts.required_fields
        request_data = request.json

        for field, field_object in fields.items():
            if not field_object.null:
                if request_data.get(field) is None or (request.method == 'POST' and field not in request_data):
                    return self.response_json(status_code=400,
                                              message=response_messages.ErrorNonNullableFieldInsert.format(field, required_fields))

            if field in request_data:
                if hasattr(field_object, 'max_length'):
                    max_length = field_object.max_length
                    if len(request_data.get(field)) > max_length:
                        return self.response_json(status_code=400,
                                                  message=response_messages.ErrorFieldOutOfRange.format(field, 0, max_length))

        return True

    def _validate_field_size(self, request):
        shortcuts = self.model.shortcuts
        response_messages = self.config.response_messages
        request_data = request.json

        for key, value in request_data.items():
            field_type = shortcuts.editable_fields.get(key).db_field
            if field_type == 'int':
                min_size = -2147483647
                max_size = 2147483647
            elif field_type == 'bigint':
                min_size = -9223372036854775808
                max_size = 9223372036854775807
            else:
                continue

            if not min_size <= value <= max_size:
                return self.response_json(status_code=400,
                                          message=response_messages.ErrorFieldOutOfRange.format(key, min_size, max_size))

        return True

