from app.forms import SteuerlotseBaseForm
from app.forms.multistep_flow import FormStep, SectionHeaderWithList
from app.forms.fields import ConfirmationField

from flask_babel import _
from flask_babel import lazy_gettext as _l


class StepSectionEinwilligung(SectionHeaderWithList):
    name = 'section_einwilligung'

    def __init__(self, **kwargs):
        super(StepSectionEinwilligung, self).__init__(
            title=_('form.lotse.section-einwilligung-title'),
            intro=_('form.lotse.section-einwilligung-intro'),
            **kwargs,
            list_items=[
                _('form.lotse.section-einwilligung-item-1'),
                _('form.lotse.section-einwilligung-item-2'),
            ])


class StepDeclarationIncomes(FormStep):
    name = 'decl_incomes'

    class Form(SteuerlotseBaseForm):
        declaration_incomes = ConfirmationField(_l('form.lotse.field_declaration_incomes'))

    def __init__(self, **kwargs):
        super(StepDeclarationIncomes, self).__init__(
            title=_('form.lotse.declaration-incomes-title'),
            intro=_('form.lotse.declaration-incomes-intro'),
            form=self.Form,
            template='lotse/form_declaration_incomes.html',
            **kwargs,
        )


class StepDeclarationEdaten(FormStep):
    name = 'decl_edaten'

    class Form(SteuerlotseBaseForm):
        declaration_edaten = ConfirmationField(_l('form.lotse.field_declaration_edaten'))

    def __init__(self, **kwargs):
        super(StepDeclarationEdaten, self).__init__(
            title=_('form.lotse.declaration-edaten-title'),
            intro=_('form.lotse.declaration-edaten-intro'),
            form=self.Form,
            template='lotse/form_declaration_edaten.html',
            **kwargs,
        )
