# This is here to allow a sub-object that contains all of our crud information within the
# peewee model and avoid messing with model object data as much as possible


class ResponseMessages:
    # Errors
    # TODO change these values to use the filed instead
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
        'notin': 'field is not in list'
    }

    response_messages = ResponseMessages()


# Internal class only used to shortcut a variety of things
class CrudShortcuts(object):
    def __init__(self, model):
        self.table_name = model._meta.db_table
        self.fields = model._meta.fields
        self.model = model

    @property
    def primary_key(self):
        for key, value in self.fields.items():
            if value.primary_key:
                return key

    @property
    def primary_key_type(self):
        pk_field = self.fields.get(self.primary_key).get_column_type()

        column_type = pk_field.replace(' ', '')
        column_type = column_type.replace('AUTO_INCREMENT', '')

        types = {
            'INTEGER': 'int',
            'SERIAL': 'int',
            'VARCHAR': 'str'
        }

        return types.get(column_type, None)

    @property
    def base_uri(self):
        return '/{}'.format(self.table_name)

    @property
    def required_fields(self):
        required_fields = []
        for field, field_object in self.editable_fields.items():
            if not field_object.null:
                required_fields.append(field)

        return required_fields

    @property
    def editable_fields(self):
        fields = {}
        for key, value in self.model._meta.fields.items():
            if self.primary_key == key:
                continue

            fields[key] = value
        return fields
