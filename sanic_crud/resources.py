import traceback
from math import ceil

from playhouse.shortcuts import model_to_dict
from sanic.log import log
from sanic.views import HTTPMethodView

from sanic_crud.helpers import response_json, collection_filter, validation, get_model


class _BaseResource(HTTPMethodView):
    pass


# Resource for multiple objects
class BaseCollectionResource(_BaseResource):
    model = None

    @collection_filter
    async def get(self, request, **kwargs):
        try:
            config = self.model.crud_config
            response_messages = config.response_messages

            # Verify page is an int
            try:
                page = int(request.args.get('page', 1))
            except ValueError:
                return response_json(status_code=400,
                                     message=response_messages.ErrorTypeInteger.format('page'))

            include_foreign_keys = True if 'foreign_keys' in request.args \
                                           and request.args['foreign_keys'][0] == 'true' else False

            results = []
            data = kwargs.get('filtered_results')
            total_records = data.count()
            total_pages = ceil(total_records / config.COLLECTION_MAX_RESULTS_PER_PAGE)
            data = data.paginate(page, config.COLLECTION_MAX_RESULTS_PER_PAGE)

            for row in data:
                results.append(model_to_dict(row, backrefs=include_foreign_keys))

            return response_json(data=results,
                                 status_code=200,
                                 message=response_messages.SuccessOk,
                                 page=page,
                                 total_pages=total_pages)
        except Exception as e:
            log.error(traceback.print_exc())
            return response_json(message=str(e),
                                 status_code=500)

    @validation
    async def post(self, request):
        response_messages = self.model.crud_config.response_messages

        try:
            result = self.model.create(**request.json)
            return response_json(data=model_to_dict(result),
                                 status_code=200,
                                 message=response_messages.SuccessRowCreated.format(result.id)
                                 )
        except Exception as e:
            log.error(traceback.print_exc())
            return response_json(message=str(e),
                                 status_code=500)


# Resource for a single object
class BaseResource(_BaseResource):
    model = None

    async def get(self, request, **kwargs):
        try:
            shortcuts = self.model.shortcuts
            response_messages = self.model.crud_config.response_messages

            primary_key = kwargs.get(shortcuts.primary_key)
            include_foreign_keys = True if 'foreign_keys' in request.args \
                                           and request.args['foreign_keys'][0] == 'true' else False

            data = get_model(primary_key=primary_key, model=self.model)

            if not data:
                return response_json(data=data,
                                     status_code=404,
                                     message=response_messages.ErrorDoesNotExist.format(primary_key))
            else:
                return response_json(data=model_to_dict(data, backrefs=include_foreign_keys),
                                     status_code=200,
                                     message=response_messages.SuccessOk)
        except Exception as e:
            log.error(traceback.print_exc())
            return response_json(message=str(e),
                                 status_code=500)

    @validation
    async def put(self, request, **kwargs):
        try:
            shortcuts = self.model.shortcuts
            response_messages = self.model.crud_config.response_messages

            primary_key = kwargs.get(shortcuts.primary_key)
            resource = get_model(primary_key=primary_key, model=self.model)

            if not resource:
                return response_json(data={},
                                     status_code=404,
                                     message=response_messages.ErrorDoesNotExist.format(primary_key))

            for key, value in request.json.items():
                setattr(resource, key, value)

                resource.save()

            return response_json(data=model_to_dict(resource),
                                 status_code=200,
                                 message=response_messages.SuccessOk)
        except Exception as e:
            log.error(traceback.print_exc())
            return response_json(message=str(e),
                                 status_code=500)

    async def delete(self, request, **kwargs):
        try:
            shortcuts = self.model.shortcuts
            response_messages = self.model.crud_config.response_messages

            primary_key = kwargs.get(shortcuts.primary_key)
            resource = get_model(primary_key=primary_key, model=self.model)

            if not resource:
                return response_json(data={},
                                     status_code=404,
                                     message=response_messages.ErrorDoesNotExist.format(primary_key))

            resource.delete_instance()

            return response_json(status_code=200, message=response_messages.SuccessRowDeleted.format(primary_key))
        except Exception as e:
            log.error(traceback.print_exc())
            return response_json(message=str(e),
                                 status_code=500)