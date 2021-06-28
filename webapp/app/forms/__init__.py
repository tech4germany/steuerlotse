from wtforms import Form


class SteuerlotseBaseForm(Form):
    class Meta:
        locales = ['de_DE', 'de']

        def bind_field(self, form, unbound_field, options):
            filters = unbound_field.kwargs.get('filters', [])
            filters.append(strip_input)
            return unbound_field.bind(form=form, filters=filters, **options)

    @staticmethod
    def _list_has_entries(field):
        return field.data and field.data != ['']


def strip_input(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value
