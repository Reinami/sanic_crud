from .crud_config import CrudConfig
from .single_resource import BaseResource
from .collection_resource import BaseCollectionResource
from .helpers import convert_column_type


def generate_crud(app, model_array):
    for model in model_array:
        if not hasattr(model, 'crud_config'):
            model.crud_config = CrudConfig(model)

        config = model.crud_config

        SingleResource = type('SingleResource', (BaseResource,), {'model': model})
        CollectionResource = type('CollectionResource', (BaseCollectionResource,), {'model': model})

        app.add_route(SingleResource.as_view(), model.crud_config.base_uri + '/<{}:{}>'.format(config.primary_key, config.primary_key_type))
        app.add_route(CollectionResource.as_view(), model.crud_config.base_uri)
