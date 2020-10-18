from app.forms import SteuerlotseBaseForm
from app.forms.multistep_flow import FormStep, SectionHeaderWithList
from app.forms.fields import YesNoField

from flask_babel import _
from flask_babel import lazy_gettext as _l
from wtforms import StringField, IntegerField, RadioField, DateField, SelectField, validators
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired

import app.utils


class StepSectionMeineDaten(SectionHeaderWithList):
    name = 'section_meine_daten'

    def __init__(self, **kwargs):
        super(StepSectionMeineDaten, self).__init__(
            title=_('form.lotse.section-meine-daten-title'),
            intro=_('form.lotse.section-meine-daten-intro'),
            **kwargs,
            list_items=[
                _('form.lotse.section-meine-daten-item-1'),
                _('form.lotse.section-meine-daten-item-2'),
                _('form.lotse.section-meine-daten-item-3'),
                _('form.lotse.section-meine-daten-item-4'),
                _('form.lotse.section-meine-daten-item-5'),
            ])


class StepSteuernummer(FormStep):
    name = 'steuernummer'

    class Form(SteuerlotseBaseForm):
        steuernummer = StringField(_l('form.lotse.steuernummer'), [InputRequired()])

    def __init__(self, **kwargs):
        super(StepSteuernummer, self).__init__(
            title=_l('form.lotse.steuernummer-title'),
            form=self.Form,
            **kwargs,
            template='form_label.html'
        )


class StepFamilienstand(FormStep):
    name = 'familienstand'

    class Form(SteuerlotseBaseForm):
        familienstand = RadioField(
            label=_l('form.lotse.field_familienstand'),
            choices=[
                ('single', _l('form.lotse.familienstand-single')),
                ('married', _l('form.lotse.familienstand-married')),
                ('widowed', _l('form.lotse.familienstand-widowed')),
                ('divorced', _l('form.lotse.familienstand-divorced')),
                ('separated', _l('form.lotse.familienstand-separated')),
            ],
            validators=[InputRequired()]
        )
        familienstand_date = DateField(_l('form.lotse.familienstand_date'), validators=())

        def validate_familienstand_date(self, field):
            if self.familienstand.data == 'single':
                validators.Optional()(self, field)
            else:
                validators.InputRequired(_l('form.lotse.validation-familienstand-date'))(self, field)

    def __init__(self, **kwargs):
        super(StepFamilienstand, self).__init__(
            title=_l('form.lotse.familienstand-title'),
            form=self.Form,
            **kwargs,
            template='lotse/form_familienstand.html'
        )


class StepPersonA(FormStep):
    name = 'person_a'

    class Form(SteuerlotseBaseForm):
        person_a_idnr = StringField(
            _l('form.lotse.field_person_idnr'), [InputRequired()],
            render_kw={'help': _l('form.lotse.field_person_idnr-help')})
        person_a_dob = DateField(_l('form.lotse.field_person_dob'), [InputRequired()])
        person_a_first_name = StringField(_l('form.lotse.field_person_first_name'), [InputRequired()])
        person_a_last_name = StringField(_l('form.lotse.field_person_last_name'), [InputRequired()])
        person_a_street = StringField(_l('form.lotse.field_person_street'), [InputRequired()])
        person_a_street_number = IntegerField(_l('form.lotse.field_person_street_number'), [InputRequired()])
        person_a_street_number_ext = StringField(_l('form.lotse.field_person_street_number_ext'))
        person_a_address_ext = StringField(_l('form.lotse.field_person_address_ext'))
        person_a_plz = IntegerField(_l('form.lotse.field_person_plz'), [InputRequired()])
        person_a_town = StringField(_l('form.lotse.field_person_town'), [InputRequired()])
        person_a_religion = SelectField(_l('form.lotse.field_person_religion'), choices=[
            ('none', _l('form.lotse.field_person_religion-none')),
            ('ev', _l('form.lotse.field_person_religion-ev')),
            ('rk', _l('form.lotse.field_person_religion-rk')),
            ('ak', _l('form.lotse.field_person_religion-ak')),
        ], validators=[InputRequired()], render_kw={'help': _l('form.lotse.field_person_religion-help')})

        person_a_beh_grad = IntegerField(_l('form.lotse.field_person_beh_grad'), [validators.Optional()],
                                         render_kw={'help': _l('form.lotse.field_person_beh_grad-help')})
        person_a_blind = YesNoField(_l('form.lotse.field_person_blind'))

    def __init__(self, **kwargs):
        super(StepPersonA, self).__init__(
            title=_('form.lotse.person-a-title'),
            intro=_('form.lotse.person-a-intro'),
            form=self.Form,
            **kwargs,
            template='lotse/form_person_a.html'
        )

    def next_step(self, data):
        if show_person_b(data):
            return StepPersonB
        else:
            return StepIban


def show_person_b(data):
    return data['familienstand'] in ('married')


class StepPersonB(FormStep):
    name = 'person_b'

    class Form(SteuerlotseBaseForm):
        def input_required_if_not_same_address(form, field):
            if form.person_b_same_address.data == 'yes':
                validators.Optional()(form, field)
            else:
                validators.InputRequired()(form, field)

        person_b_idnr = StringField(
            _l('form.lotse.field_person_idnr'), [InputRequired()],
            render_kw={'help': _l('form.lotse.field_person_idnr-help')})
        person_b_dob = DateField(_l('form.lotse.field_person_dob'), [InputRequired()])
        person_b_first_name = StringField(_l('form.lotse.field_person_first_name'), [InputRequired()])
        person_b_last_name = StringField(_l('form.lotse.field_person_last_name'), [InputRequired()])

        person_b_same_address = RadioField(_l('form.lotse.field_person_b_same_address'), choices=[
            ('yes', _l('form.lotse.field_person_b_same_address-yes')),
            ('no', _l('form.lotse.field_person_b_same_address-no')),
        ])
        person_b_street = StringField(_l('form.lotse.field_person_street'), [input_required_if_not_same_address])
        person_b_street_number = IntegerField(_l('form.lotse.field_person_street_number'), [
                                              input_required_if_not_same_address])
        person_b_street_number_ext = StringField(_l('form.lotse.field_person_street_number_ext'))
        person_b_address_ext = StringField(_l('form.lotse.field_person_address_ext'))
        person_b_plz = IntegerField(_l('form.lotse.field_person_plz'), [input_required_if_not_same_address])
        person_b_town = StringField(_l('form.lotse.field_person_town'), [input_required_if_not_same_address])

        person_b_religion = SelectField(_l('form.lotse.field_person_religion'), choices=[
            ('none', _l('form.lotse.field_person_religion-none')),
            ('ev', _l('form.lotse.field_person_religion-ev')),
            ('rk', _l('form.lotse.field_person_religion-rk')),
            ('ak', _l('form.lotse.field_person_religion-ak')),
        ], validators=[InputRequired()], render_kw={'help': _l('form.lotse.field_person_religion-help')})

        person_b_beh_grad = IntegerField(_l('form.lotse.field_person_beh_grad'), [validators.Optional()],
                                         render_kw={'help': _l('form.lotse.field_person_beh_grad-help')})
        person_b_blind = YesNoField(_l('form.lotse.field_person_blind'))

    def __init__(self, **kwargs):
        super(StepPersonB, self).__init__(
            title=_('form.lotse.person-b-title'),
            intro=_('form.lotse.person-b-intro'),
            form=self.Form,
            **kwargs,
            template='lotse/form_person_b.html'
        )


class StepIban(FormStep):
    name = 'iban'

    class Form(SteuerlotseBaseForm):
        iban = StringField(_l('form.lotse.field_iban'), [InputRequired()])

        def validate_iban(form, field):
            validators.InputRequired()(form, field)
            app.utils.validate_iban(field.data)

    def __init__(self, **kwargs):
        super(StepIban, self).__init__(
            title=_l('form.lotse.iban-title'),
            intro=_l('form.lotse.iban-intro'),
            form=self.Form,
            **kwargs,
            template='form_label.html'
        )
