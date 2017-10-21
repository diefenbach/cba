import copy
import json
import logging
import uuid
from collections import OrderedDict

from django.template.loader import render_to_string

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from cba import get_request

from . utils import LazyEncoder

logger = logging.getLogger(__name__)


class Component(object):
    """Base class of all components.

        attributes
            A dictonary of HTML attributes, e.g.::

                {"style": "color:red"}

        cols
            If given the component is rendered to the width of given cols.
            The outer component has to be a grid. Defaults to ``None``.

        css_class
            The css class of the component. A string.

        component_value
            Can be used to provide a value to the component which can be
            requested within handlers. Defaults to the id of component.

        disabled
            If ``True`` the component is disabled. Defaults to ``False``

        displayed
            if ``False`` the component is hidden. Defaults to ``False``.

        draggable
            if ``True``the component can be dragged and dropped. Defaults to
            ``False``.

        droppable
            if ``True`` the other components can be dropped to the component.
            Defaults to ``False``.

        id
            The unique id of the component. This must be unique troughout
            the whole application. If the id is not given a UUID4 based
            id is created automatically.

        handler
            A dictonary with events and handlers, e.g.::

                handlers = {
                    "click": "server:handle_save",
                    "change": "client:my_js_function",
                }

            The events could be any javascript event. The handler could
            be a method of the component instance which has "catched" the
            event or one of it's parent components (handler with the prefix
            ``server``) or a javascript method ( handler with the prefix
            ``client``).

        initial_components
            The initial sub components of this component.

        is_grid
            If set to True the component provides a grid. Defaults to ``False``.

        javascript
            If given this is rendered with the component. Defaults to empty
            string.

        parent
            The parent component of the component. This is set automically
            Only the root component has a parent of `None`.

        template
            The path to the template which is used to render the component.

        remove_after_render
            If true the component is removed from the component tree after
            it has been rendered.
    """
    template = None
    remove_after_render = False

    def __init__(self, id=None, component_value=None, attributes=None,
                 css_class=None, disabled=False, displayed=True, draggable=False,
                 droppable=False, handler=None, initial_components=None, cols=None,
                 is_grid=False, javascript="", *args, **kwargs):
        self.id = id or str(uuid.uuid4())
        self.component_value = component_value
        self.attributes = attributes or {}
        self.css_class = css_class
        self.disabled = disabled
        self.displayed = displayed
        self.draggable = draggable
        self.droppable = droppable
        self.handler = handler or {}
        self.initial_components = initial_components or []
        self.javascript = javascript
        self.cols = cols
        self.is_grid = is_grid

        self.parent = None

        # Internal dictonary to hold the sub components of the component.
        self._components = OrderedDict()

        # Internal attribute to collect html of refreshed.
        self._html = None

        # Internal attribute to collect messages which should be displayed to
        # the user.
        self._messages = []

        if initial_components:
            self.initial_components = initial_components
        else:
            self.init_components()

        self._add_components()

        self.after_initial_components()

    def add_component(self, component):
        """Adds the given component to the current component.

        component
            The component which should be added.
        """
        component.parent = self
        self._components[component.id] = component

    def add_message(self, message, type="info"):
        """Adds a message.

        All messages are displayed to the user after the current request has
        been returned to the browser.
        """
        self.get_root()._messages.append({
            "text": message,
            "type": type,
        })

    def after_initial_components(self):
        """Hook which can be overriden by sub classes.
        """
        pass

    def clear(self):
        """Clears the component. Can be overriden by sub classes to clear
        specific values.
        """
        pass

    @property
    def components(self):
        """Returns all direct child components of the current component as a
        list.
        """
        return self._components.values()

    @classmethod
    def clear_session(cls):
        request = cls.get_request()
        del request.session["cba"]

    def get_component(self, id, direct_only=False, with_root=True):
        """Returns the component with the passed id.

        Starts the search within the sub components of this component (but see
        also ``with_root``).

        id
            The unique id of the component which should be returned.

        direct_only
            If set to True only the direct sub components of this component are
            taken into account. Otherwise all child components of the component
            sub tree will be taken into account.

        with_root
            If true a second search is started with root as base.
        """
        component = self._components.get(id)
        if component:
            return component
        elif direct_only is False:
            for component in self.components:
                temp = component.get_component(id, direct_only, with_root)
                if temp:
                    return temp

        # In case nothing has been found we try the parents also.
        if with_root:
            return self.get_root().get_component(id, with_root=False)

    def get_root(self):
        """Returns the root component.
        """
        if self.parent is None:
            return self
        else:
            component = self
            while component.parent:
                component = component.parent
            return component

    def get_request(self):
        """Returns the current request.
        """
        return get_request()

    def get_user(self):
        """Returns the current user.
        """
        try:
            return self.get_request().user
        except AttributeError:
            return None

    def init_components(self):
        """Can be overriden to set the initial sub components of the current
        components.
        """
        pass

    def is_root(self):
        """Returns True if the component is the root component.
        """
        if self.parent:
            return False
        else:
            return True

    def refresh(self):
        """Rerenders the current component once the current request is returned
        to the browser.
        """
        self._html = ["#{}".format(self.id), self.render()]

    def refresh_all(self):
        """Refresh the component and reloads the initial sub components.
        """
        self._components.clear()
        self.init_components()
        self._add_components()
        self._html = ["#{}".format(self.id), self.render()]

    def remove_component(self, id):
        """Removes a component from sub components of the current component.
        Returns ``True`` when it was successfully, otherwise ``False``.

        id
            The id of the component which should be removed.
        """
        try:
            del self._components[id]
        except KeyError:
            return False
        else:
            return True

    def replace_component(self, id, component):
        """Replaces a component with another.

        id
            The id of the component which should be replaced.

        component
            The component which should replace the removed one.
        """
        old_component = self.get_component(id)
        parent = old_component.parent
        parent.remove_component(id)
        parent.add_component(component)

    def render(self):
        """Renders the current component as HTML.
        """
        if self.template:
            if self.remove_after_render:
                del self.parent._components[self.id]

            return render_to_string(self.template, {
                "self": self,
            })
        else:
            return ""

    def _add_components(self):
        """Adds initial components into the default components structure.
        """
        if self.initial_components:
            logger.debug("Components loading for {}:".format(self.id))

        for component in self.initial_components:
            logger.debug("\t- {}".format(component.id))
            self.add_component(component)

        if self.initial_components:
            self.initial_components = []


class CBAView(View):
    """The default base class.

    All views of an cba application should be inherit from this class.
    """
    template = "cba/main.html"

    def __init__(self, **kwargs):
        super(CBAView, self).__init__(**kwargs)
        self._html = []
        self._messages = []

    def get(self, *args, **kwargs):
        """Handles the starting get request.
        """
        # Remove any CBA related stuff from session.
        try:
            del self.request.session["cba"]
        except KeyError:
            pass

        # Create root element and render it
        self.root = self.root(id="root")
        content = self.root.render()

        if "root" not in self.request.session:
            self.request.session["root"] = {}

        self.request.session["root"]["0"] = self.root
        self.request.session.modified = True

        return render(self.request, self.template, {
            "content": content,
        })

    def post(self, *args, **kwargs):
        """Handles all subsequent ajax calls.
        """
        if self.request.POST.get("action") == "reload":
            state = str(self.request.POST.get("state"))
            self.root = self.request.session["root"][state]
            self.root.refresh()
            self._collect_components_data(self.root)
        else:
            new_state = "0"
            # new_state = str(self.request.POST.get("state"))
            # state = str(int(new_state) - 1)
            # self.root = copy.deepcopy(self.request.session["root"][state])

            self.root = self.request.session["root"]["0"]

            self._clear_components_data(self.root)
            self._load_data(self.root)

            # component_id is always the event triggering component. For DnD this
            # means component_id is the droppable and source_id is the dragged
            # item. For non DnD events source_id is None.
            handler = self.request.POST.get("handler")
            element_id = self.request.POST.get("element_id")
            component_id = self.request.POST.get("component_id")
            component_value = self.request.POST.get("component_value")
            source_id = self.request.POST.get("source_id")
            key_code = self.request.POST.get("key_code")

            component = self.root.get_component(component_id)

            logger.debug("Handler: {} / Component: {}".format(handler, component))
            import pdb; pdb.set_trace()
            # Bubbles up the components to find the handler
            handler_found = False
            while component:
                if hasattr(component, handler):
                    component.element_id = element_id
                    component.component_id = component_id
                    component.component_value = component_value
                    component.source_id = source_id
                    component.key_code = key_code
                    getattr(component, handler)()
                    handler_found = True
                    break
                component = component.parent

            if handler_found is False:
                logger.error("Handler {} not found".format(handler))
                raise AttributeError("Handler {} not found".format(handler))

            self._collect_components_data(self.root)
            logger.debug("Refreshed components: {}".format(self._html))
            logger.debug("Collected messages: {}".format(self._messages))

            self.request.session["root"][new_state] = self.root
            self.request.session.modified = True

        return HttpResponse(
            json.dumps(
                {
                    "html": self._html,
                    "messages": self._messages,
                },
                cls=LazyEncoder
            ),
            content_type='application/json'
        )

    def _clear_components_data(self, root):
        """Clears messsage and html of all components.
        """
        root._html = []
        root._messages = []
        if hasattr(root, "components"):
            for component in root.components:
                component._html = ""
                component._messages = []
                self._clear_components_data(component)

    def _collect_components_data(self, component):
        """Collects refreshed HTML and messages from all components.
        """
        if component.is_root():
            if component._html:
                self._html.append(component._html)

            if component._messages:
                self._messages.extend(component._messages)

        if hasattr(component, "components"):
            for component in component.components:
                if component._html:
                    self._html.append(component._html)
                if component._messages:
                    self._messages.extend(component._messages)
                self._collect_components_data(component)

    def _load_data(self, root):
        """Loads components with values from the browser.
        """
        logger.debug("load data for {}".format(root))
        if hasattr(root, "components"):
            for component in root.components:
                if component.id in self.request.POST:
                    root._components[component.id].value = self.request.POST.get(component.id)
                else:
                    # List elements
                    list_id = "{}[]".format(component.id)
                    if list_id in self.request.POST:
                        root._components[component.id].value = self.request.POST.getlist(list_id)
                    else:
                        # if the component not within the request at the value
                        # is deleted
                        pass
                        # root._components[component.id].value = ""

                if component.id in self.request.FILES:
                    if component.multiple:
                        root._components[component.id].value = self.request.FILES.getlist(component.id)
                    else:
                        root._components[component.id].value = self.request.FILES.get(component.id)

                # The FileInput component sends ids of images which should be delete. Per
                # convention these are send with the key "delete"-<component.id>.
                if "delete-{}[]".format(component.id) in self.request.POST:
                    root._components[component.id].to_delete = self.request.POST.getlist("delete-{}[]".format(component.id))

                self._load_data(component)
