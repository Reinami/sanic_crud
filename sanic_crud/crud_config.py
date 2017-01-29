# This is here to allow a sub-object that contains all of our crud information within the
# peewee model and avoid messing with model object data as much as possible


class CrudConfig(object):
    COLLECTION_MAX_RESULTS_PER_PAGE = 100

    def __init__(self, model):
        self.metadata = model._meta
        self.table_name = self.metadata.db_table
        self.fields = self.metadata.fields
        self.required_fields = [field for field in self.get_field_names() if not self.fields.get(field).null]
        self.primary_key = self._get_primary_key()
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
