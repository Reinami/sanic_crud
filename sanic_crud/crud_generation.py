from .config import CrudConfig, CrudShortcuts
from .resources.single_resource import BaseResource
from .resources.collection_resource import BaseCollectionResource


def generate_crud(app, model_array):
    for model in model_array:
        if not hasattr(model, 'crud_config'):
            model.crud_config = CrudConfig

        shortcuts = CrudShortcuts(model)
        model.shortcuts = shortcuts

        SingleResource = type('SingleResource', (BaseResource,), {'model': model})
        CollectionResource = type('CollectionResource', (BaseCollectionResource,), {'model': model})

        app.add_route(SingleResource.as_view(), shortcuts.base_uri + '/<{}:{}>'.format(shortcuts.primary_key, shortcuts.primary_key_type))
        app.add_route(CollectionResource.as_view(), shortcuts.base_uri)
