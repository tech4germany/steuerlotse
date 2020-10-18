from decimal import Decimal
from flask.templating import render_template
from jinja2.runtime import markup_join
from wtforms import RadioField, Field, validators
from wtforms.fields.core import BooleanField
from wtforms.validators import InputRequired
from wtforms.widgets.core import TextInput, Markup, html_params

from flask_babel import _
from babel.numbers import format_decimal, parse_decimal


class EuroFieldWidget(TextInput):
    "A simple Euro widget that uses Bootstrap features for nice looks."

    def __call__(self, field, **kwargs):
        kwargs['class'] = 'euro_field form-control'
        markup_input = super(EuroFieldWidget, self).__call__(field, **kwargs)
        markup = Markup(
            Markup('<div class="input-group">') +
            markup_input +
            Markup('<div class="input-group-append"><span class="input-group-text">€</span></div>') +
            Markup('</div>')
        )
        return markup


class EuroField(Field):
    """The Euro field will use Bootstrap features to display the currency symbol, work with German
    locale and internally handles the entry as a Decimal."""
    widget = EuroFieldWidget()

    def __init__(self, label, locale='de_DE', **kwargs):
        super(EuroField, self).__init__(label, **kwargs)
        self.locale = locale
        self.default_value = ''

    def _value(self):
        if self.data in (None, ''):
            return self.default_value
        else:
            return format_decimal(self.data, locale=self.locale).replace('.', '')

    def process_formdata(self, raw_data):
        if not raw_data or not raw_data[0]:
            self.data = None
        else:
            self.data = Decimal(parse_decimal(raw_data[0], locale=self.locale))


class ConfirmationField(BooleanField):
    """A CheckBox that will not validate unless checked."""

    def __init__(self, label=None, false_values=None, **kwargs):
        super(BooleanField, self).__init__(
            label,
            validators=(InputRequired(message=_('confirmation_field_must_be_set')),),
            **kwargs
        )

class JqueryEntriesWidget(object):
    """A custom multi-entry widget that is based on jquery."""
    html_params = staticmethod(html_params)

    def __init__(self):
        self.input_type = None

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('data', field.data)
        kwargs.setdefault('split_chars', field.split_chars)
        kwargs.setdefault('add_button_text', _('jquery_entries.add'))
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        if 'required' not in kwargs and 'required' in getattr(field, 'flags', []):
            kwargs['required'] = True
        return Markup(render_template('fields/jquery_entries.html', kwargs=kwargs))


class EntriesField(Field):
    """The entries field will display its internal `list` data through multiple
    input text boxes where the user can add and remove items."""
    widget = JqueryEntriesWidget()
    split_chars = '~~~'

    def _value(self):
        if self.data:
            return self.split_chars.join(self.data)
        else:
            return ''

    def _split(self, string):
        return [x.strip() for x in string.split(self.split_chars)]

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self._split(valuelist[0])
        else:
            self.data = []


class YesNoWidget(object):
    """A simple switch-box that allows to choose between yes and no."""

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if 'required' not in kwargs and 'required' in getattr(field, 'flags', []):
            kwargs['required'] = True

        # TODO use proper HTML generation
        html = ""
        html += '<div class="btn-group btn-group-toggle" data-toggle="buttons">\n'

        for choice in field.choices:
            value, desc = choice
            html += '<label class="btn btn-secondary switch-%s">' % value
            html += '<input type="radio" %s>' % html_params(
                name=field.name,
                value=value,
                checked=(field.data == value),
                **kwargs
            )
            html += desc
            html += '</label>\n'

        html += '</div>\n'

        return Markup(html)


class YesNoField(RadioField):
    def __init__(self, label='', validators=None, **kwargs):
        kwargs['choices'] = [('yes', _('switch.yes')), ('no', _('switch.no'))]
        super(YesNoField, self).__init__(label, validators, **kwargs)
        self.widget = YesNoWidget()