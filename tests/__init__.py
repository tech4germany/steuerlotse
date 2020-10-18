import os
os.environ["FLASK_ENV"] = 'testing'

from tests.app.elster.est_mapping import *
from tests.app.elster.elster_xml import *
from tests.app.elster.elster_service import *
from tests.app.elster.pyeric_dispatcher import *
from tests.app.elster.sample_data_validations import *

from tests.app.forms.lotse.flow_lotse import *
from tests.app.forms.session_manager import *
from tests.pyeric.eric import *
