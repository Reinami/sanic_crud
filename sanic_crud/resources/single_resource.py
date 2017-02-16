import traceback

from playhouse.shortcuts import model_to_dict
from sanic.log import log

from ..resources.base_resource import BaseResource


# Resource for a single object
class BaseSingleResource(BaseResource):
    async def get(self, request, **kwargs):
        try:
            shortcuts = self.model.shortcuts
            response_messages = self.config.response_messages

            primary_key = kwargs.get(shortcuts.primary_key)
            include_backrefs = True if 'backrefs' in request.args \
                                       and request.args['backrefs'][0] == 'true' else False
            include_foreign_keys = True if 'foreign_keys' in request.args \
                                           and request.args['foreign_keys'][0] == 'true' else False

            data = self.get_model(primary_key)

            if not data:
                return self.response_json(data=data,
                                          status_code=404,
                                          message=response_messages.ErrorDoesNotExist.format(primary_key))
            else:
                return self.response_json(data=model_to_dict(data, recurse=include_foreign_keys, backrefs=include_backrefs),
                                          status_code=200,
                                          message=response_messages.SuccessOk)
        except Exception as e:
            log.error(traceback.print_exc())
            return self.response_json(message=str(e),
                                      status_code=500)

    async def put(self, request, **kwargs):
        valid_request = self.validate_request(request)

        if valid_request is not True:
            return valid_request

        try:
            shortcuts = self.model.shortcuts
            response_messages = self.config.response_messages
            request_data = request.json.items()

            primary_key = kwargs.get(shortcuts.primary_key)
            resource = self.get_model(primary_key)

            if not resource:
                return self.response_json(data={},
                                          status_code=404,
                                          message=response_messages.ErrorDoesNotExist.format(primary_key))

            for key, value in request_data:
                setattr(resource, key, value)

            resource.save()

            return self.response_json(data=model_to_dict(resource),
                                      status_code=200,
                                      message=response_messages.SuccessOk)
        except Exception as e:
            log.error(traceback.print_exc())
            return self.response_json(message=str(e),
                                      status_code=500)

    async def delete(self, request, **kwargs):
        try:
            shortcuts = self.model.shortcuts
            response_messages = self.config.response_messages

            primary_key = kwargs.get(shortcuts.primary_key)
            resource = self.get_model(primary_key)

            if not resource:
                return self.response_json(data={},
                                          status_code=404,
                                          message=response_messages.ErrorDoesNotExist.format(primary_key))

            resource.delete_instance()

            return self.response_json(status_code=200, message=response_messages.SuccessRowDeleted.format(primary_key))
        except Exception as e:
            log.error(traceback.print_exc())
            return self.response_json(message=str(e),
                                      status_code=500)