from app.forms import SteuerlotseBaseForm
from app.forms.multistep_flow import MultiStepFlow, FormStep, DisplayStep, RenderInfo
from app.forms.fields import YesNoField

from collections import namedtuple
from flask import render_template
from flask_babel import _
from flask_babel import lazy_gettext as _l


class EligibilityStepStart(DisplayStep):
    name = 'welcome'

    def __init__(self, **kwargs):
        super(EligibilityStepStart, self).__init__(
            title=_('form.eligibility.start-title'),
            intro=_('form.eligibility.start-intro'), **kwargs)

    def render(self, data, render_info):
        return render_template('eligibility/display_start.html', render_info=render_info)


class EligibilityStepIncomes(FormStep):
    name = 'incomes'

    class IncomesForm(SteuerlotseBaseForm):
        renten = YesNoField(_l('form.eligibility.income-renten'),
                            render_kw={'help': _l('form.eligibility.income-renten-help')})
        pensionen = YesNoField(_l('form.eligibility.income-pensionen'))
        geringf = YesNoField(_l('form.eligibility.income-geringf'))
        kapitaleink = YesNoField(_l('form.eligibility.income-kapital'))
        other = YesNoField(_l('form.eligibility.income-other'))

    def __init__(self, **kwargs):
        super(EligibilityStepIncomes, self).__init__(
            title=_('form.eligibility.income-title'),
            form=self.IncomesForm,
            **kwargs)

    def next_step(self, data):
        result = get_eligibility_result(data)
        if result.eligible:
            return EligibilityStepSuccess
        else:
            return EligibilityStepFailure


class EligibilityStepFailure(DisplayStep):
    name = 'failure'

    def __init__(self, **kwargs):
        kwargs['prev_step'] = EligibilityStepIncomes
        super(EligibilityStepFailure, self).__init__(title=_('form.eligibility.failure-title'), **kwargs)

    def render(self, data, render_info):
        result = get_eligibility_result(data)
        return render_template(
            'eligibility/display_failure.html',
            render_info=render_info,
            reasons=result.reasons)


class EligibilityStepSuccess(DisplayStep):
    name = 'success'

    def __init__(self, **kwargs):
        kwargs['prev_step'] = EligibilityStepIncomes
        super(EligibilityStepSuccess, self).__init__(title=_('form.eligibility.success-title'), **kwargs)

    def render(self, data, render_info):
        result = get_eligibility_result(data)
        return render_template(
            'eligibility/display_success.html',
            render_info=render_info,
            reasons=result.reasons)


EligibilityResult = namedtuple(
    typename='EligibilityResult',
    field_names=['eligible', 'reasons']
)


def get_eligibility_result(data):
    if 'other' in data:
        if data['other'] == 'yes':
            return EligibilityResult(False, [_('form.eligibility.reason-other-income')])

        reasons = []
        if data['renten'] == 'yes' or data['pensionen'] == 'yes':
            reasons += [_('form.eligibility.reason-rente-pension')]
        if data['geringf'] == 'yes':
            reasons += [_('form.eligibility.reason-other-geringf')]
        if data['kapitaleink'] == 'yes':
            reasons += [_('form.eligibility.reason-other-kapital')]
        reasons += [_('form.eligibility.reason-no-other-income')]
        return EligibilityResult(True, reasons)

    return EligibilityResult(None, [])


class EligibilityMultiStepFlow(MultiStepFlow):

    def __init__(self, endpoint):
        super(EligibilityMultiStepFlow, self).__init__(
            title=_('form.eligibility.title'),
            steps=[
                EligibilityStepStart,
                EligibilityStepIncomes,
                EligibilityStepFailure,
                EligibilityStepSuccess,
            ],
            endpoint=endpoint,
        )
