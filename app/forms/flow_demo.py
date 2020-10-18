from app.forms import SteuerlotseBaseForm
from app.forms.multistep_flow import MultiStepFlow, FormStep, DisplayStep, RenderInfo
from app.forms.fields import EuroField, EntriesField

from collections import namedtuple
from decimal import Decimal
from flask import render_template
from flask_babel import _
from flask_babel import lazy_gettext as _l
from wtforms import RadioField
from wtforms.widgets.core import html_params


class StepHello(DisplayStep):
    name = 'hello'

    def __init__(self, **kwargs):
        super(StepHello, self).__init__(title=_('form.demo.hello-title'), **kwargs)

    def render(self, data, render_info):
        return render_template('demo/hello.html', render_info=render_info)


class StepFruit(FormStep):
    name = 'fruit'

    class Form(SteuerlotseBaseForm):
        fav_fruit = RadioField(
            label=_l('form.demo.radio-fruit'),
            choices=[
                ('apple', _('form.demo.radio-fruit-apple')),
                ('orange', _('form.demo.radio-fruit-organe'))
            ],
            render_kw={'help': 'Animals are great!'}
        )

    def __init__(self, **kwargs):
        super(StepFruit, self).__init__(
            title=_('form.demo.fruit-title'),
            form=self.Form,
            template='form_single.html',
            **kwargs
        )


class StepEuro(FormStep):
    name = 'euro'

    class Form(SteuerlotseBaseForm):
        summe_einnahmen = EuroField(label=_l('form.demo.einnahmen'))
        summe_ausgaben = EuroField(label=_l('form.demo.ausgaben'))

    def __init__(self, **kwargs):
        super(StepEuro, self).__init__(
            title=_('form.demo.euro-title'),
            form=self.Form,
            **kwargs
        )


class StepEntries(FormStep):
    name = 'entries'

    class Form(SteuerlotseBaseForm):
        animals = EntriesField(label='Your favourite animals', default=['Monkey', 'Penguin'])

    def __init__(self, **kwargs):
        super(StepEntries, self).__init__(
            title='Animals!',
            intro='Which ones do you like the most?',
            form=self.Form,
            template='demo/form_entries.html',
            **kwargs
        )

class StepEnd(DisplayStep):
    name = 'end'

    def __init__(self, **kwargs):
        super(StepEnd, self).__init__(title=_('form.demo.end-title'), **kwargs)

    def render(self, data, render_info):
        return render_template('demo/end.html', render_info=render_info)


class DemoMultiStepFlow(MultiStepFlow):

    def __init__(self, endpoint):
        super(DemoMultiStepFlow, self).__init__(
            title=_('form.demo.title'),
            steps=[
                StepHello,
                StepEuro,
                StepFruit,
                StepEntries,
                StepEnd
            ],
            endpoint=endpoint,
        )

    def debug_data(self):
        return (
            StepEuro,
            {}
        )
