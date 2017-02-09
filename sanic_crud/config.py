# This is here to allow a sub-object that contains all of our crud information within the
# peewee model and avoid messing with model object data as much as possible
from sanic_crud.helpers import convert_column_type


class ResponseMessages:
    # Errors
    ErrorDoesNotExist = 'Resource with id \'{}\' does not exist'
    ErrorTypeInteger = 'Value \'{}\' must be an integer'
    ErrorTypeBoolean = 'Value \'{}\' must be a boolean: 0 or 1'
    ErrorTypeDatetime = 'Value \'{}\' must be a datetime: YYYY-mm-dd HH:MM:SS or integer'
    ErrorTypeList = 'Value \'{}\' must be a comma separated list'
    ErrorPrimaryKeyUpdateInsert = 'Field: \'id\' cannot be inserted or modified, field is primary key'
    ErrorInvalidField = 'Field: \'{}\' does not exist choices are {}'
    ErrorNonNullableFieldInsert = 'Field: \'{}\' cannot be null, required fields are: {}'
    ErrorInvalidJSON = 'Invalid JSON input'
    ErrorInvalidFilterOption = 'Invalid Filter Option: {}, valid options are {}'
    ErrorFieldOutOfRange = 'Invalid range for field \'{}\', must be between {} and {}'

    # Success
    SuccessOk = 'OK'
    SuccessRowUpdated = 'Resource with id \'{}\' was updated!'
    SuccessRowCreated = 'Resource with id \'{}\' was created!'
    SuccessRowDeleted = 'Resource with id \'{}\' was deleted!'


class CrudConfig(object):
    COLLECTION_MAX_RESULTS_PER_PAGE = 100

    # {'filter_key': 'human readable description'}
    FILTER_OPTIONS = {
        'startswith': 'field starts with value',
        'contains': 'field contains value',
        'lt': 'field is less than value',
        'lte': 'field is less than or equal to value',
        'gt': 'field is greater than value',
        'gte': 'field is greater than or equal to value',
        'null': 'field is null',
        '=': 'field is equal to value',
        'in': 'field is in list',
        'notin': 'field is not in list',
        'page': 'Page number for pagination'
    }

    response_messages = ResponseMessages()


# Internal class only used to shortcut a variety of things
class CrudShortcuts(object):
    def __init__(self, model):
        self.metadata = model._meta
        self.table_name = self.metadata.db_table
        self.fields = self.metadata.fields
        self.required_fields = [field for field in self.get_field_names() if not self.fields.get(field).null]
        self.primary_key = self._get_primary_key()
        self.primary_key_type = convert_column_type(self.fields.get(self.primary_key).get_column_type())
        self.base_uri = self._generate_base_uri()

    def _get_primary_key(self):
        for key, value in self.fields.items():
            if value.primary_key:
                return key

    def _generate_base_uri(self):
        return '/{}'.format(self.table_name)

    def get_field_names(self, exclude_primary_key=True):
        field_names = list(self.fields.keys())

        if exclude_primary_key:
            # TODO: this seems to fail when using self.primary_key, find out why
            field_names.remove(self._get_primary_key())

        return field_names
