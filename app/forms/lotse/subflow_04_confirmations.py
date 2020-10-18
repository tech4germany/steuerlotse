from flask.globals import session
from app.forms import SteuerlotseBaseForm
from app.forms.multistep_flow import FormStep, DisplayStep, FlowNavItem, SectionHeaderWithList
from app.forms.fields import ConfirmationField

from collections import namedtuple
from decimal import Decimal
from flask import render_template, redirect
from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask.helpers import url_for


class StepSectionConfirmation(SectionHeaderWithList):
    name = 'section_confirmation'

    def __init__(self, **kwargs):
        super(StepSectionConfirmation, self).__init__(
            title=_('form.lotse.section-confirmation-title'),
            intro=_('form.lotse.section-confirmation-intro'),
            **kwargs,
            list_items=[
                _('form.lotse.section-confirmation-item-1'),
                _('form.lotse.section-confirmation-item-2'),
                _('form.lotse.section-confirmation-item-3'),
                _('form.lotse.section-confirmation-item-4'),
            ])


class StepConfirmation(FormStep):
    name = 'confirmation'

    class Form(SteuerlotseBaseForm):
        confirm_complete_correct = ConfirmationField(_l('form.lotse.field_confirm_complete_correct'))
        confirm_send = ConfirmationField(_l('form.lotse.field_confirm_send'))

    def __init__(self, **kwargs):
        super(StepConfirmation, self).__init__(
            title=_('form.lotse.confirmation-title'),
            form=self.Form,
            template='lotse/form_confirmation.html',
            **kwargs,
        )

class StepSending(DisplayStep):
    name = 'sending'

    def __init__(self, **kwargs):
        super(StepSending, self).__init__(title=_('form.lotse.ack-sending'), **kwargs)

    def render(self, data, render_info):
        try:
            from app.elster.elster_service import send_with_elster
            send_with_elster(data, render_info.session)
        except Exception:
            # we ignore it here and let the next page handle this
            pass

        return redirect(render_info.next_url)


class StepAck(DisplayStep):
    name = 'ack'

    def __init__(self, **kwargs):
        super(StepAck, self).__init__(title=_('form.lotse.ack-title'), **kwargs)

    def render(self, data, render_info):
        from app.elster.pyeric_dispatcher import was_successful, get_transfer_ticket, get_eric_response, get_server_response

        eric_data = {}
        eric_data['was_successful'] = was_successful(render_info.session)
        eric_data['pdf_link'] = url_for('download_pdf', session=render_info.session)
        eric_data['eric_response'] = get_eric_response(render_info.session)
        eric_data['server_response'] = get_server_response(render_info.session)

        eric_data['transfer_ticket'] = get_transfer_ticket(eric_data['server_response'])

        return render_template('lotse/display_ack.html', render_info=render_info, eric_data=eric_data)


class StepFail(DisplayStep):
    name = 'ack'

    def __init__(self, **kwargs):
        super(StepAck, self).__init__(title=_('form.lotse.ack-title'), **kwargs)

    def render(self, data, render_info):
        return render_template('lotse/display_fail.html', render_info=render_info)
