from .config import CrudConfig, CrudShortcuts
from .resources import BaseSingleResource
from .resources import BaseCollectionResource


def generate_crud(app, model_array):
    for model in model_array:
        if not hasattr(app, 'crud_config'):
            config = CrudConfig
        else:
            config = model.crud_config

        # Some handy shortcuts
        shortcuts = CrudShortcuts(model)
        model.shortcuts = shortcuts

        SingleResource = type('SingleResource', (BaseSingleResource,), {'model': model, 'config': config})
        CollectionResource = type('CollectionResource', (BaseCollectionResource,), {'model': model, 'config': config})

        app.add_route(SingleResource.as_view(), shortcuts.base_uri + '/<{}:{}>'.format(shortcuts.primary_key, shortcuts.primary_key_type))
        app.add_route(CollectionResource.as_view(), shortcuts.base_uri)
