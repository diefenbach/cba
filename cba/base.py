import logging
import uuid
from collections import OrderedDict

from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class Component(object):
    """Base class of all components.

        attributes
            A dictonary of HTML attributes, e.g.::

                {"style": "color:red"}

        css_class
            The css class of the component. A string.

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

    def __init__(self, id=None, attributes=None, css_class=None, handler=None, initial_components=None, *args, **kwargs):
        self.id = id or str(uuid.uuid4())
        self.attributes = attributes or {}
        self.css_class = css_class
        self.handler = handler or {}
        self.initial_components = initial_components or []

        self.parent = None
        self._components = OrderedDict()
        self._html = None
        self._messages = []

        if initial_components:
            self.initial_components = initial_components
        else:
            self.init_components()

        self._add_components()

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

    def get_from_session(self, key, default=None):
        """Gets a value from the session.

            key
                The key under which the value has been saved. When the key
                doesn't exist the method returns ``default``.

            default
                The value the method returns if key is not existing.
        """
        request = self.get_request()
        return request.session.get(key, default)

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
        from cba import get_request
        return get_request()
        try:
            return self.get_root().request
        except AttributeError:
            return None

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
        self._components = OrderedDict()
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

    def set_to_session(self, key, value):
        """Saves a value to the session.

            key
                The key under which the value is saved.
            value
                The value to be saved.
        """
        request = self.get_request()
        request.session[key] = value

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
