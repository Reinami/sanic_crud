import traceback
from math import ceil

from playhouse.shortcuts import model_to_dict
from sanic.log import log

from ..resources.base_resource import BaseResource


def collection_filter(func):
    def wrapped(self, request, *args, **kwargs):
        model = self.model
        config = model.crud_config
        response_messages = config.response_messages

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
                return self.response_json(status_code=400,
                                          message=response_messages.ErrorInvalidFilterOption.format(comparison, model.shortcuts.FILTER_OPTIONS))

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


# Resource for multiple objects
class BaseCollectionResource(BaseResource):
    @collection_filter
    async def get(self, request, **kwargs):
        valid_request = self.validate_request(request)

        if valid_request is not True:
            return valid_request

        try:
            response_messages = self.config.response_messages

            # Verify page is an int
            try:
                page = int(request.args.get('page', 1))
            except ValueError:
                return self.response_json(status_code=400,
                                          message=response_messages.ErrorTypeInteger.format('page'))

            include_foreign_keys = True if 'foreign_keys' in request.args \
                                           and request.args['foreign_keys'][0] == 'true' else False

            results = []
            data = kwargs.get('filtered_results')
            total_records = data.count()
            total_pages = ceil(total_records / self.config.COLLECTION_MAX_RESULTS_PER_PAGE)
            data = data.paginate(page, self.config.COLLECTION_MAX_RESULTS_PER_PAGE)

            for row in data:
                results.append(model_to_dict(row, backrefs=include_foreign_keys))

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
