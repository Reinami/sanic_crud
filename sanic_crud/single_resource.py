from .base_resource import _BaseResource
from .helpers import response_json, get_model, validation
from .messages import ErrorDoesNotExist, SuccessRowDeleted, SuccessOk
from playhouse.shortcuts import model_to_dict
from sanic.log import log
import traceback


# Resource for a single object
class BaseResource(_BaseResource):
    model = None

    def get(self, request, **kwargs):
        try:
            primary_key = kwargs.get('id')
            include_foreign_keys = True if 'foreign_keys' in request.args \
                                           and request.args['foreign_keys'][0] == 'true' else False

            data = get_model(primary_key=primary_key, model=self.model)

            if not data:
                return response_json(data=data,
                                     status_code=404,
                                     message=ErrorDoesNotExist.format(primary_key))
            else:
                return response_json(data=model_to_dict(data, backrefs=include_foreign_keys),
                                     status_code=200,
                                     message=SuccessOk)
        except Exception as e:
            log.error(traceback.print_exc())
            return response_json(message=str(e),
                                 status_code=500)

    @validation
    def put(self, request, **kwargs):
        try:
            primary_key = kwargs.get('id')
            resource = get_model(primary_key=primary_key, model=self.model)

            if not resource:
                return response_json(data={},
                                     status_code=404,
                                     message=ErrorDoesNotExist.format(primary_key))

            for key, value in request.json.items():
                setattr(resource, key, value)

                resource.save()

            return response_json(data=model_to_dict(resource),
                                 status_code=200,
                                 message=SuccessOk)
        except Exception as e:
            log.error(traceback.print_exc())
            return response_json(message=str(e),
                                 status_code=500)

    def delete(self, request, **kwargs):
        try:
            primary_key = kwargs.get('id')
            resource = get_model(primary_key=primary_key, model=self.model)

            if not resource:
                return response_json(data={},
                                     status_code=404,
                                     message=ErrorDoesNotExist.format(primary_key))

            resource.delete_instance()

            return response_json(status_code=200, message=SuccessRowDeleted.format(primary_key))
        except Exception as e:
            log.error(traceback.print_exc())
            return response_json(message=str(e),
                                 status_code=500)