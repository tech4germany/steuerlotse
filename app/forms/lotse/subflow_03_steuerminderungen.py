from app.forms import SteuerlotseBaseForm
from app.forms.multistep_flow import FormStep, SectionHeaderWithList
from app.forms.fields import EntriesField, EuroField

from flask import render_template
from flask_babel import _
from flask_babel import lazy_gettext as _l
from wtforms import RadioField
from wtforms.validators import InputRequired


class StepSectionSteuerminderung(SectionHeaderWithList):
    name = 'section_steuerminderung'

    def __init__(self, **kwargs):
        super(StepSectionSteuerminderung, self).__init__(
            title=_('form.lotse.section-steuerminderung-title'),
            intro=_('form.lotse.section-steuerminderung-intro'),
            **kwargs,
            list_items=[
                _('form.lotse.section-steuerminderung-item-1'),
                _('form.lotse.section-steuerminderung-item-2'),
                _('form.lotse.section-steuerminderung-item-3'),
            ])


class StepSteuerminderungYesNo(FormStep):
    name = 'steuerminderung_yesno'

    class Form(SteuerlotseBaseForm):

        steuerminderung = RadioField(
            label=_l('form.lotse.field_steuerminderung'),
            choices=[
                ('yes', _l('form.lotse.field_steuerminderung-yes')),
                ('no', _l('form.lotse.field_steuerminderung-no')),
            ],
            validators=[InputRequired()]
        )

    def __init__(self, **kwargs):
        super(StepSteuerminderungYesNo, self).__init__(
            title=_l('form.lotse.steuerminderung-title'),
            intro=_l('form.lotse.steuerminderung-intro'),
            form=self.Form,
            template='lotse/form_steuerminderung_yesno.html',
            **kwargs,
        )

    def next_step(self, data):
        if data['steuerminderung'] == 'no':
            from app.forms.lotse.subflow_04_confirmations import StepSectionConfirmation
            return StepSectionConfirmation
        else:
            return super(StepSteuerminderungYesNo, self).next_step(data)


class StepSubSectionHealth(SectionHeaderWithList):
    name = 'subsection_health'

    def __init__(self, **kwargs):
        super(StepSubSectionHealth, self).__init__(
            title=_('form.lotse.subsection-health-title'),
            intro=_('form.lotse.subsection-health-intro'),
            **kwargs,
            list_items=[
                _('form.lotse.subsection-health-item-1'),
                _('form.lotse.subsection-health-item-2'),
            ])


class StepVorsorge(FormStep):
    name = 'vorsorge'

    class Form(SteuerlotseBaseForm):
        vorsorge_summe = EuroField(
            _l('form.lotse.field_vorsorge_summe'),
            render_kw={'help': _l('form.lotse.field_vorsorge_summe-help')})

    def __init__(self, **kwargs):
        super(StepVorsorge, self).__init__(
            title=_('form.lotse.vorsorge-title'),
            intro=_('form.lotse.vorsorge-intro'),
            form=self.Form,
            template='lotse/form_aufwendungen_with_list.html',
            **kwargs,
        )

    def render(self, form, data, render_info):
        return render_template(self.template, form=form, render_info=render_info, list_items=[
            _('form.lotse.vorsorge-list-item-1'),
            _('form.lotse.vorsorge-list-item-2'),
            _('form.lotse.vorsorge-list-item-3'),
        ])


class StepAussergBela(FormStep):
    name = 'ausserg_bela'

    class Form(SteuerlotseBaseForm):
        aussergbela_entries = EntriesField(_l('form.lotse.field_aussergbela_entries'), default=[''],
                                           render_kw={'help': _l('form.lotse.field_aussergbela_entries-help')})
        aussergbela_summe_aufw = EuroField(_l('form.lotse.field_aussergbela_summe_aufw'))
        aussergbela_ansprueche = EuroField(_l('form.lotse.field_aussergbela_ansprueche'))

    def __init__(self, **kwargs):
        super(StepAussergBela, self).__init__(
            title=_('form.lotse.ausserg_bela-title'),
            intro=_('form.lotse.ausserg_bela-intro'),
            form=self.Form,
            template='form_label.html',
            **kwargs,
        )


class StepSubSectionHousehold(SectionHeaderWithList):
    name = 'subsection_household'

    def __init__(self, **kwargs):
        super(StepSubSectionHousehold, self).__init__(
            title=_('form.lotse.subsection-household-title'),
            intro=_('form.lotse.subsection-household-intro'),
            **kwargs,
            list_items=[
                _('form.lotse.subsection-household-item-1'),
                _('form.lotse.subsection-household-item-2'),
            ])


class StepHaushaltsnahe(FormStep):
    name = 'haushaltsnahe'

    class Form(SteuerlotseBaseForm):
        haushaltsnahe_entries = EntriesField(_l('form.lotse.field_haushaltsnahe_entries'), default=[''],
                                             render_kw={'help': _l('form.lotse.field_haushaltsnahe_entries-help')})
        haushaltsnahe_summe = EuroField(_l('form.lotse.field_haushaltsnahe_summe'))

    def __init__(self, **kwargs):
        super(StepHaushaltsnahe, self).__init__(
            title=_('form.lotse.haushaltsnahe-title'),
            intro=_('form.lotse.haushaltsnahe-intro'),
            form=self.Form,
            template='lotse/form_aufwendungen_with_list.html',
            **kwargs,
        )

    def render(self, form, data, render_info):
        return render_template(self.template, form=form, render_info=render_info, list_items=[
            _('form.lotse.haushaltsnahe-list-item-1'),
            _('form.lotse.haushaltsnahe-list-item-2'),
            _('form.lotse.haushaltsnahe-list-item-3'),
            _('form.lotse.haushaltsnahe-list-item-4'),
        ])


class StepHandwerker(FormStep):
    name = 'handwerker'

    class Form(SteuerlotseBaseForm):
        handwerker_entries = EntriesField(_l('form.lotse.field_handwerker_entries'), default=[''],
                                          render_kw={'help': _l('form.lotse.field_handwerker_entries-help')})
        handwerker_summe = EuroField(_l('form.lotse.field_handwerker_summe'))
        handwerker_lohn_etc_summe = EuroField(_l('form.lotse.field_handwerker_lohn_etc_summe'))

    def __init__(self, **kwargs):
        super(StepHandwerker, self).__init__(
            title=_('form.lotse.handwerker-title'),
            intro=_('form.lotse.handwerker-intro'),
            form=self.Form,
            template='lotse/form_aufwendungen_with_list.html',
            **kwargs,
        )

    def render(self, form, data, render_info):
        return render_template(self.template, form=form, render_info=render_info, list_items=[])


class StepSubSectionSpenden(SectionHeaderWithList):
    name = 'subsection_spenden'

    def __init__(self, **kwargs):
        super(StepSubSectionSpenden, self).__init__(
            title=_('form.lotse.subsection-spenden-title'),
            intro=_('form.lotse.subsection-spenden-intro'),
            **kwargs,
            list_items=[
                _('form.lotse.subsection-spenden-item-1'),
                _('form.lotse.subsection-spenden-item-2'),
            ])


class StepReligion(FormStep):
    name = 'religion'

    class Form(SteuerlotseBaseForm):
        religion_paid_summe = EuroField(
            _l('form.lotse.field_religion_paid_summe'),
            render_kw={'help': _l('form.lotse.field_religion_paid_summe-help')})
        religion_reimbursed_summe = EuroField(_l('form.lotse.field_religion_reimbursed_summe'))

    def __init__(self, **kwargs):
        super(StepReligion, self).__init__(
            title=_('form.lotse.religion-title'),
            intro=_('form.lotse.religion-intro'),
            form=self.Form,
            template='lotse/form_aufwendungen_with_list.html',
            **kwargs,
        )

    def render(self, form, data, render_info):
        return render_template(self.template, form=form, render_info=render_info, list_items=[])


class StepSpenden(FormStep):
    name = 'spenden'

    class Form(SteuerlotseBaseForm):
        spenden_inland = EuroField(
            _l('form.lotse.spenden-inland'),
            render_kw={'help': _l('form.lotse.spenden-help')})
        spenden_inland_parteien = EuroField(_l('form.lotse.spenden-inland-parteien'))

    def __init__(self, **kwargs):
        super(StepSpenden, self).__init__(
            title=_('form.lotse.spenden-inland-title'),
            intro=_('form.lotse.spenden-inland-intro'),
            form=self.Form,
            template='form_label.html',
            **kwargs,
        )
