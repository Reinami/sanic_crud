import traceback

from playhouse.shortcuts import model_to_dict
from sanic.log import log

from ..resources.base_resource import _BaseResource
from ..helpers import response_json, get_model, validation


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