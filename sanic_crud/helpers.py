from datetime import datetime
from sanic.response import json
from sanic.log import log


def collection_filter(func):
    def wrapped(self, request, *args, **kwargs):
        model = self.model
        shortcuts = model.shortcuts
        config = model.crud_config

        fields = shortcuts.editable_fields
        response_messages = self.model.crud_config.response_messages

        query = model.select()

        # Iterate over args and split the filters
        for key, value in request.args.items():
            # skip over include foreign_keys flag
            if key == 'foreign_keys':
                continue

            filter_parts = key.split('__')
            field = filter_parts[0]
            comparison = '='

            if field == 'page':
                continue

            # If the length is 2, then there is a filter component
            if len(filter_parts) == 2:
                comparison = filter_parts[1]

            # Validate that a supported comparison is used
            if comparison not in config.FILTER_OPTIONS:
                return response_json(status_code=400,
                                     message=response_messages.ErrorInvalidFilterOption.format(comparison, shortcuts.FILTER_OPTIONS))

            # Validate that the field is part of the table
            if field not in fields:
                return response_json(status_code=400,
                                     message=response_messages.ErrorInvalidField.format(key, fields.keys()))

            # Validate that the value is the correct type
            if comparison in ['in', 'notin']:
                value = value.split(',')

            if comparison != 'null':
                for item in value:
                    field_type_invalid = _validate_field_type(model, fields.get(field), item)
                    if field_type_invalid:
                        return field_type_invalid

            model_field = getattr(model, field)

            # Build the query from comparisons
            if comparison == '=':
                query = query.where(model_field == value)
            elif comparison == 'null':
                query = query.where(model_field.is_null(True if value == 1 else False))
            elif comparison == 'startswith':
                query = query.where(model_field.startswith(value))
            elif comparison == 'contains':
                query = query.where(model_field.contains(value))
            elif comparison == 'lt':
                query = query.where(model_field < value)
            elif comparison == 'lte':
                query = query.where(model_field <= value)
            elif comparison == 'gt':
                query = query.where(model_field > value)
            elif comparison == 'gte':
                query = query.where(model_field >= value)
            elif comparison == 'in':
                query = query.where(model_field << value)
            elif comparison == 'notin':
                query = query.where(~(model_field << value))

        kwargs['filtered_results'] = query

        return func(self, request, *args, **kwargs)

    return wrapped


# Helper function, takes in a database field and an input value to make sure the input is the correct type for the db
def _validate_field_type(response_messages, field, value):
    expected_field_type = field.db_field

    if expected_field_type in ['int', 'bool']:
        try:
            int(value)
        except (ValueError, TypeError):
            return response_json(status_code=400,
                                 message=response_messages.ErrorTypeInteger.format(value) if expected_field_type == 'int' else response_messages.ErrorTypeBoolean.format(value))

    elif expected_field_type == 'datetime':
        try:
            int(value)
        except ValueError:
            try:
                datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                return response_json(status_code=400,
                                     message=response_messages.ErrorTypeDatetime.format(value))

    return False


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

    response = json(response_data, status=status_code)

    return response


# Gets a model with a primary key
def get_model(primary_key, model):
    try:
        pk_field = model.shortcuts.primary_key
        return model.get(getattr(model, pk_field) == primary_key)
    except model.DoesNotExist:
        return {}
