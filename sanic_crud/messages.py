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

# Errors
ErrorDoesNotExist = 'Resource with id \'{}\' does not exist'
ErrorTypeInteger = 'Value \'{}\' must be an integer'
ErrorTypeBoolean = 'Value \'{}\' must be a boolean: 0 or 1'
ErrorTypeDatetime = 'Value \'{}\' must be a datetime: YYYY-mm-dd HH:MM:SS'
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

MAX_RESULTS_PER_PAGE = 100