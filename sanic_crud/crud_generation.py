from .table import CrudTable
from .single_resource import BaseResource
from .collection_resource import BaseCollectionResource


def generate_crud(app, model_array):
    for model in model_array:
        if not hasattr(model, 'crud_config'):
            model.crud_config = CrudTable(model)

        SingleResource = type('SingleResource', (BaseResource,), {'model': model})
        CollectionResource = type('CollectionResource', (BaseCollectionResource,), {'model': model})

        app.add_route(SingleResource.as_view(), model.crud_config.base_uri + '/<id:int>')
        app.add_route(CollectionResource.as_view(), model.crud_config.base_uri)
