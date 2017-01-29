# This is here to allow a sub-object that contains all of our crud information within the
# peewee model and avoid messing with model object data as much as possible


class CrudTable(object):
    def __init__(self, model):
        self.metadata = model._meta
        self.table_name = self.metadata.db_table
        self.fields = self.metadata.fields
        self.primary_key = self._get_primary_key()
        self.base_uri = self._generate_base_uri()

    def _get_primary_key(self):
        for key, value in self.fields.items():
            if value.primary_key:
                return key

    def _generate_base_uri(self):
        return '/{}'.format(self.table_name)