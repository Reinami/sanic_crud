from sanic_crud.config import CrudConfig, CrudShortcuts
from sanic_crud.resources import BaseResource
from sanic_crud.resources import BaseCollectionResource


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
