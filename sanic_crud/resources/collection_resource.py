import traceback
from math import ceil
import datetime

from playhouse.shortcuts import model_to_dict
from sanic.log import log

from ..resources.base_resource import BaseResource


def collection_filter(func):
    def wrapped(self, request, *args, **kwargs):
        model = self.model
        shortcuts = model.shortcuts

        fields = shortcuts.fields
        response_messages = self.config.response_messages

        query = model.select()

        # Iterate over args and split the filters
        for key, value in request.args.items():
            # skip over include foreign_keys flag
            if key == 'foreign_keys' or key == 'backrefs':
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
            if comparison not in self.config.FILTER_OPTIONS:
                return self.response_json(status_code=400,
                                          message=response_messages.ErrorInvalidFilterOption.format(comparison, shortcuts.FILTER_OPTIONS))

            # Validate that the field is part of the table
            if field not in fields:
                return self.response_json(status_code=400,
                                          message=response_messages.ErrorInvalidField.format(key, fields.keys()))

            # Validate that the value is the correct type
            if comparison in ['in', 'notin']:
                value = value.split(',')

            if comparison != 'null':
                for item in value:
                    field_type_invalid = _validate_field_type(self, model, fields.get(field), item)
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
def _validate_field_type(self, field, value):
    expected_field_type = field.db_field
    response_messages = self.model.crud_config.response_messages

    if expected_field_type in ['int', 'bool']:
        try:
            int(value)
        except (ValueError, TypeError):
            return self.response_json(status_code=400,
                                      message=response_messages.ErrorTypeInteger.format(value) if expected_field_type == 'int' else response_messages.ErrorTypeBoolean.format(value))

    elif expected_field_type == 'datetime':
        try:
            int(value)
        except Exception:
            try:
                datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                return self.response_json(status_code=400,
                                          message=response_messages.ErrorTypeDatetime.format(value))

    return False


# Resource for multiple objects
class BaseCollectionResource(BaseResource):
    @collection_filter
    async def get(self, request, **kwargs):
        try:
            response_messages = self.config.response_messages

            # Verify page is an int
            try:
                page = int(request.args.get('page', 1))
            except ValueError:
                return self.response_json(status_code=400,
                                          message=response_messages.ErrorTypeInteger.format('page'))

            include_backrefs = True if 'backrefs' in request.args \
                                       and request.args['backrefs'][0] == 'true' else False
            include_foreign_keys = True if 'foreign_keys' in request.args \
                                           and request.args['foreign_keys'][0] == 'true' else False

            results = []
            data = kwargs.get('filtered_results')
            total_records = data.count()
            total_pages = ceil(total_records / self.config.COLLECTION_MAX_RESULTS_PER_PAGE)
            data = data.paginate(page, self.config.COLLECTION_MAX_RESULTS_PER_PAGE)

            for row in data:
                results.append(model_to_dict(row, recurse=include_foreign_keys, backrefs=include_backrefs))

            return self.response_json(data=results,
                                      status_code=200,
                                      message=response_messages.SuccessOk,
                                      page=page,
                                      total_pages=total_pages)
        except Exception as e:
            log.error(traceback.print_exc())
            return self.response_json(message=str(e),
                                      status_code=500
                                      )

    async def post(self, request):
        valid_request = self.validate_request(request)

        if valid_request is not True:
            return valid_request

        try:
            result = self.model.create(**request.json)
            return self.response_json(data=model_to_dict(result),
                                      status_code=200,
                                      message=self.config.response_messages.SuccessRowCreated.format(result.id)
                                      )
        except Exception as e:
            log.error(traceback.print_exc())
            return self.response_json(message=str(e),
                                      status_code=500
                                      )
