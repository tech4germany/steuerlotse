from app.forms.multistep_flow import MultiStepFlow, DisplayStep, FlowNavItem
from app.forms.lotse.subflow_01_declarations import *
from app.forms.lotse.subflow_02_personal_data import *
from app.forms.lotse.subflow_03_steuerminderungen import *
from app.forms.lotse.subflow_04_confirmations import *

from decimal import Decimal
from flask import render_template
from flask_babel import _

import datetime


class StepSummary(DisplayStep):
    name = 'summary'

    def __init__(self, **kwargs):
        super(StepSummary, self).__init__(
            title=_('form.lotse.summary-title'),
            intro=_('form.lotse.summary-intro'),
            **kwargs,
        )
        self.flow = LotseMultiStepFlow(None)
        self.sections = [
            StepSectionEinwilligung,
            StepSectionMeineDaten,
            StepSectionSteuerminderung,
            StepSectionConfirmation,
        ]
        self.ignore = [
            StepVorsorge,
            StepAussergBela,
            StepHaushaltsnahe,
            StepHandwerker,
            StepReligion,
            StepSpenden,
        ]

    def render(self, data, render_info):
        # dict of the form `{ section: (section_url, [(step1, url1), ...]), ...}`
        sections_steps = {}
        flow = self.flow
        curr_section, curr_section_steps = None, []

        for step in flow.steps.values():
            if step in self.ignore:
                continue

            # If we hit a section header, save current (if any) and start new section
            if step in self.sections:
                if curr_section:
                    sections_steps[flow._load_step(curr_section.name)] = (
                        self.url_for_step(curr_section, _link_overview=True),
                        [
                            (flow._load_step(s.name), self.url_for_step(s))
                            for s in curr_section_steps
                        ]
                    )

                curr_section = step
                curr_section_steps = []
                continue

            # Otherwise it's a normal step and we add it to the current section
            curr_section_steps.append(step)

        return render_template('lotse/display_summary.html',
                               render_info=render_info, sections_steps=sections_steps)

_DEBUG_DATA = (
            StepSummary,
            {
                'steuernummer': '9198011310010',
                'familienstand': 'married',
                'familienstand_date': datetime.date(2000, 1, 31),

                'person_a_idnr': '10000100001',
                'person_a_dob': datetime.date(1950, 8, 16),
                'person_a_first_name': 'Manfred',
                'person_a_last_name': 'Mustername',
                'person_a_street': 'Steuerweg',
                'person_a_street_number': 42,
                'person_a_plz': 20354,
                'person_a_town': 'Hamburg',
                'person_a_religion': 'none',
                'person_a_blind': 'no',

                'person_b_idnr': '10000100002',
                'person_b_dob': datetime.date(1951, 2, 25),
                'person_b_first_name': 'Gerta',
                'person_b_last_name': 'Mustername',
                'person_b_same_address': 'yes',
                'person_b_religion': 'rk',
                'person_b_blind': 'no',

                'iban': 'DE35133713370000012345',

                'steuerminderung': 'yes',
                
                'haushaltsnahe_entries': ["Gartenarbeiten"],
                'haushaltsnahe_summe': Decimal('500.00'),

                'handwerker_entries': ["Renovierung Badezimmer"],
                'handwerker_summe': Decimal('200.00'),
                'handwerker_lohn_etc_summe': Decimal('100.00'),

                'confirm_complete_correct': True,
                'confirm_send': True,
            }
        )

class LotseMultiStepFlow(MultiStepFlow):

    def __init__(self, endpoint):
        super(LotseMultiStepFlow, self).__init__(
            title=_('form.lotse.title'),
            endpoint=endpoint,
            steps=[
                StepSectionEinwilligung,
                StepDeclarationIncomes,
                StepDeclarationEdaten,

                StepSectionMeineDaten,
                StepSteuernummer,
                StepFamilienstand,
                StepPersonA,
                StepPersonB,
                StepIban,

                StepSectionSteuerminderung,
                StepSteuerminderungYesNo,
                StepSubSectionHealth,
                StepVorsorge,
                StepAussergBela,
                StepSubSectionHousehold,
                StepHaushaltsnahe,
                StepHandwerker,
                StepSubSectionSpenden,
                StepReligion,
                StepSpenden,

                StepSectionConfirmation,
                StepSummary,
                StepConfirmation,
                StepSending,
                StepAck,
            ],
            overview_step = StepSummary,
        )

    def _get_flow_nav(self, active_step):
        sections = [
            StepSectionEinwilligung,
            StepSectionMeineDaten,
            StepSectionSteuerminderung,
            StepSectionConfirmation
        ]

        # Determine the active index based on name matching
        active_index = -1
        for step in self.steps.values():
            if step in sections:
                active_index += 1
            if step.name == active_step.name:
                break

        # Create nav items list and set the `active` flag according to `active_index`
        items = []
        for index, section in enumerate(sections):
            items.append(FlowNavItem(
                number=index+1,
                text=self._load_step(section.name).title,
                active=(index == active_index)
            ))

        return items

    def debug_data(self):
        return _DEBUG_DATA
