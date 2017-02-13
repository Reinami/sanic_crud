import traceback
from math import ceil

from playhouse.shortcuts import model_to_dict
from sanic.log import log

from ..resources.base_resource import BaseResource
from ..helpers import collection_filter


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
