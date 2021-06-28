from flask_babel import _
from wtforms import HiddenField

from app.forms import SteuerlotseBaseForm
from app.forms.steps.step import FormStep


class LogoutInputStep(FormStep):
    name = 'data_input'

    class Form(SteuerlotseBaseForm):
        hidden = HiddenField(label='')

    def __init__(self, **kwargs):
        super(LogoutInputStep, self).__init__(
            title=_('form.logout.input-title'),
            intro=_('form.logout.input-intro'),
            form=self.Form,
            **kwargs,
            header_title=_('form.logout.header-title'),
            template='basis/form_full_width.html')
