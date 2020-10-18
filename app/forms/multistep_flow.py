from collections import namedtuple
from flask import redirect, request, render_template, url_for

from app.forms.session_manager import InMemorySessionManager, MongoDbSessionManager
from app import app

# The RenderInfo is provided to all templates
RenderInfo = namedtuple(
    typename='RenderInfo',
    field_names=['flow_title', 'step_title', 'step_intro',
                 'prev_url', 'next_url', 'submit_url', 'flow_nav',
                 'session', 'overview_url']
)

# Used for the header step overview of the main form
FlowNavItem = namedtuple(
    typename='FlowNavItem',
    field_names=['number', 'text', 'active'],
    defaults=[False]
)


class MultiStepFlow(object):
    """A MultiStepFlow represents a form with individual screens. The current
    context is maintained through a `session` URL parameter that is passed along.
    This allows it to gracefully handle forced refreshs and back/forward navigation
    in the browser. The current state is maintained via a `SessionManager`.
    """

    def __init__(self, title, steps, endpoint, overview_step=None):
        """Creates a new MultistepFlow for the given configuration.

        The steps are a list of `FormStep` subclasses.
        This allows to initialise only the steps necessary and to use the
        the declared ordering for initializing `prev_step` and `next_step`.
        """
        self.title = title
        self.steps = {s.name: s for s in steps}
        self.first_step = next(iter(self.steps.values()))
        self.overview_step = overview_step

        self.endpoint = endpoint

        if app.env == 'production':
            self.sessions = MongoDbSessionManager()
        else:
            self.sessions = InMemorySessionManager()

    def _load_step(self, step_name):
        step_names, step_types = list(self.steps.keys()), list(self.steps.values())
        idx = step_names.index(step_name)

        # By default set `prev_step` and `next_step` in order of definition
        return self.steps[step_name](
            prev_step=step_types[idx - 1] if idx > 0 else '',
            next_step=step_types[idx + 1] if idx < len(step_types) - 1 else ''
        )

    def _get_flow_nav(self, active_step):
        """Implementer can override this function to show a navigation on top of the
        form. The returned data type is a list of `FlowNavItem`."""
        return None

    def handle(self, step_name):
        session = request.args.get('session')
        link_overview = request.args.get('link_overview', False) == 'True'

        def url_for_step(step, _session=session, _link_overview=link_overview):
            """Generate URL for given step and current session."""

            # show overview buttons if explicitely requested or if shown for current request
            return url_for(self.endpoint, step=step.name, session=_session, link_overview=_link_overview)

        if step_name == 'start' or not self.sessions.has_session(session):

            # Implementers can override `debug_data` to return a `step_name`
            # and `form_data` to use while testing
            dbg = self.debug_data()
            if dbg:
                session, data = self.sessions.get_or_create(None, dbg[1])
                return redirect(url_for_step(dbg[0], _session=session))
            else:
                session, data = self.sessions.get_or_create(None)
                return redirect(url_for_step(step=self.first_step, _session=session))

        step = self._load_step(step_name)
        _, data = self.sessions.get_or_create(session)

        prev_step = step.prev_step(data)

        # next step only applies to DisplayStep as the
        # FormSteps are submitting to themselves first
        display_next_step = step.next_step(
            data) if isinstance(step, DisplayStep) else None

        render_info = RenderInfo(
            flow_title=self.title,
            step_title=step.title,
            step_intro=step.intro,
            prev_url=url_for_step(prev_step) if prev_step else None,
            next_url=url_for_step(display_next_step) if display_next_step else None,
            submit_url=url_for_step(step),
            flow_nav=self._get_flow_nav(step),
            session=session,
            overview_url=url_for_step(self.overview_step) if link_overview and self.overview_step else None,
        )

        if isinstance(step, DisplayStep):
            step._hook_url_for_step(url_for_step)
            return step.render(data, render_info)

        if isinstance(step, FormStep):
            form = step.create_form(data, request)
            if request.method == 'POST' and form.validate():

                # Merge new form data with existing data
                merged_data = data
                merged_data.update(form.data)
                self.sessions.update(session, merged_data)

                next_step = step.next_step(data)
                return redirect(url_for_step(next_step))

            return step.render(form, data, render_info)

    def debug_data(self):
        return None


class Step(object):
    """An abstract step that provides default `prev_step` and `next_step`
    implementations if these are provided during construction.
    """

    def __init__(self, title, intro, prev_step=None, next_step=None):
        self.title = title
        self.intro = intro
        self._prev_step = prev_step
        self._next_step = next_step

    def prev_step(self, data):
        if self._prev_step == None:
            raise NotImplementedError()
        else:
            return self._prev_step

    def next_step(self, data):
        if self.next_step == None:
            raise NotImplementedError()
        else:
            return self._next_step


class FormStep(Step):
    """A FormStep owns a wtform and knows how to create and render it. The template
    to use can be overiden and customised.
    """

    def __init__(self, title, form, intro=None, prev_step=None, next_step=None, template='form_grid.html'):
        super(FormStep, self).__init__(title, intro, prev_step, next_step)
        self.form = form
        self.template = template

    def create_form(self, data, request):
        # fixed: If `form_data` is present it will always override `data` during
        # value binding. For `BooleanFields` an empty/missing value in the `form_data`
        # will lead to an unchecked box.
        #
        # TODO: currently does not allow for deactivating checkboxes :/
        form_data = request.form
        if len(form_data) == 0:
            form_data = None

        form = self.form(form_data, **data)
        return form

    def render(self, form, data, render_info):
        form.first_field = next(iter(form))
        return render_template(
            template_name_or_list=self.template,
            form=form,
            render_info=render_info
        )


class DisplayStep(Step):
    """The DisplayStep usually shows data that is not interactive (except from links)."""

    def __init__(self, title, intro=None, prev_step=None, next_step=None):
        super(DisplayStep, self).__init__(title, intro, prev_step, next_step)

    def _hook_url_for_step(self, fun):
        self.url_for_step = fun

    def render(self, data, render_info):
        raise NotImplementedError()


class SectionHeaderWithList(DisplayStep):

    def __init__(self, title, intro, prev_step, next_step, list_items):
        super(SectionHeaderWithList, self).__init__(
            title=title, intro=intro, prev_step=prev_step, next_step=next_step)
        self.list_items = list_items

    def render(self, data, render_info):
        return render_template(
            'lotse/section_header_with_list.html',
            render_info=render_info,
            list_items=self.list_items)
