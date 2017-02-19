from .config import CrudConfig, CrudShortcuts
from .resources import BaseSingleResource
from .resources import BaseCollectionResource
from sanic.log import log
from sanic.response import json


def generate_crud(app, model_array):
    # Setup Configuration
    base_config = app.config.crud_config if hasattr(app.config, 'crud_config') else CrudConfig
    for model in model_array:
        if not hasattr(model, 'crud_config'):
            config = base_config
        else:
            config = model.crud_config

        # Some handy shortcuts
        shortcuts = CrudShortcuts(model)
        model.shortcuts = shortcuts

        # Generate Resources and Routes
        SingleResource = type('SingleResource', (BaseSingleResource,), {'model': model, 'config': config})
        CollectionResource = type('CollectionResource', (BaseCollectionResource,), {'model': model, 'config': config})
        app.add_route(SingleResource.as_view(), shortcuts.base_uri + '/<{}:{}>'.format(shortcuts.primary_key, shortcuts.primary_key_type))
        app.add_route(CollectionResource.as_view(), shortcuts.base_uri)

    # Add base route
    app.add_route(_generate_base_route(model_array), '/', methods=['GET'])


def _generate_base_route(model_array):
    tables = {}

    for model in model_array:
        fields = []
        table_name = model.shortcuts.table_name
        required_fields = model.shortcuts.required_fields
        for field, field_object in model.shortcuts.fields.items():
            field_name = field_object.name
            field_type = field_object.get_db_field()
            is_required = field_name in required_fields or field_type == 'primary_key'

            fields.append({
                'field_name': field_name,
                'field_type': field_type,
                'is_required': is_required
            })

        tables[table_name] = {
            'route_url': '/{}'.format(table_name),
            'fields': fields
        }

    async def base_route(request):
        response_data = {
            'data': {'routes': tables},
            'status_code': 200,
            'message': 'OK'
        }

        return json(response_data, status=200)

    return base_route
