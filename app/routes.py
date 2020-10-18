from app import app, nav
from app.content.render_content import render_how_it_works
from app.forms.flow_eligibility import EligibilityMultiStepFlow
from app.forms.flow_demo import DemoMultiStepFlow
from app.forms.lotse.flow_lotse import LotseMultiStepFlow

from flask import render_template, request, send_file
from flask_babel import _
from flask_babel import lazy_gettext as _l
from werkzeug.exceptions import InternalServerError

# Navigation


class MultiEndpointItem(nav.Item):

    def __init__(self, label, endpoint, matching_endpoint_prefixes):
        super(MultiEndpointItem, self).__init__(label, endpoint)
        self.matching_endpoint_prefixes = matching_endpoint_prefixes

    @property
    def is_current(self):
        return any([request.endpoint.startswith(pfx) for pfx in self.matching_endpoint_prefixes])


nav.Bar('top', [
    nav.Item(_l('nav.home'), 'index'),
    nav.Item(_l('nav.how-it-works'), 'howitworks'),
    MultiEndpointItem(_l('nav.lotse-form'), 'login_welcome', matching_endpoint_prefixes=['login_', 'lotse']),
    nav.Item(_l('nav.about-us'), 'contact'),
])

# Multistep flows


@app.route('/eligibility/step/<step>', methods=['GET', 'POST'])
def eligibility(step):
    flow = EligibilityMultiStepFlow(endpoint='eligibility')
    return flow.handle(step_name=step)


@app.route('/demo/step/<step>', methods=['GET', 'POST'])
def demo(step):
    flow = DemoMultiStepFlow(endpoint='demo')
    return flow.handle(step_name=step)


@app.route('/lotse/step/<step>', methods=['GET', 'POST'])
def lotse(step):
    flow = LotseMultiStepFlow(endpoint='lotse')
    return flow.handle(step_name=step)


@app.route('/download_pdf/<session>/print.pdf', methods=['GET'])
def download_pdf(session):
    from app.elster.pyeric_dispatcher import get_pdf_path
    return send_file(get_pdf_path(session))

# Content


@app.route('/')
def index():
    return render_template('content/landing_page.html')


@app.route('/kontakt')
def contact():
    return render_template('content/contact.html')


@app.route('/sofunktionierts')
def howitworks():
    return render_how_it_works()


# Login


@app.route('/login/welcome')
def login_welcome():
    return render_template('login/welcome.html')


@app.route('/login/create')
def login_create():
    return render_template('login/create.html')


@app.route('/login/create-confirm')
def login_create_confirm():
    return render_template('login/create-confirm.html')


@app.route('/login/auth')
def login_auth():
    return render_template('login/auth.html')


@app.route('/login/resume')
def login_resume():
    return render_template('login/resume.html')


# General


@app.errorhandler(404)
def error_404(error):
    return render_template('error/404.html'), 404


@app.errorhandler(InternalServerError)
def error_500(error):
    return render_template('error/500.html'), 500


@app.route('/cronjob')
def cronjob():
    from app.elster.pyeric_dispatcher import clean_old_folders
    clean_old_folders()
    return "okay\n"
