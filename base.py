import logging
import uuid
from collections import OrderedDict

from django.template.loader import render_to_string

from . utils import JSCreator

logger = logging.getLogger(__name__)


class Component(object):
    """A component is a part of a HTML application.
    """
    template = None
    remove_after_render = False

    def __init__(self, id=None, request=None, initial_components=None, attributes=None, css_class=None, actions=None, event=None, *args, **kwargs):
        """Base class of all components.

            id
                The unique id of the component. This must be unique troughout
                the whole application.

            attributes
                HTML attributes of the component.

            css_class
                The css class of the component.

            initial_components
                The initial sub components of this components.

            template
                The path to the template which is used to render the component.

            actions
                A list of actions which will be performed when the user
                interacts with the component. (Not implemented yet).
        """
        self.id = id or str(uuid.uuid4())
        self.initial_components = initial_components or []
        self.attributes = attributes or {}
        self.css_class = css_class
        self.event = event
        self.request = request

        self.actions = actions or []
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
        """Adds the given component as sub component to the current component.

        component
            The component which is added to the current component
        """
        component.parent = self
        self._components[component.id] = component

    def add_message(self, message, type="info"):
        """Adds a message. All messages are displayed to the user after the
        current request has been returned to the browser.
        """
        self.get_root()._messages.append({
            "text": message,
            "type": type,
        })

    def clear(self):
        """Clears the value of the component.
        """
        pass

    @property
    def components(self):
        """Returns all direct child components of the current component as list.
        """
        return self._components.values()

    def get_component(self, id, direct_only=False, with_root=True):
        """Returns the component with the passed id.

        id
            The unique id of the component which should be returned.

        direct_only
            If set to True only the direct sub components of this component
            are taken into account. Otherwise all child components of the
            component sub tree will be taken into account.
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
                doesn't exist the method returns ``None``.
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

    def replace_with(self, component):
        """Replaces this component with the given one.

        component
            The component which should replace the removed one.
        """
        parent = self.parent
        parent.remove_component(self.id)
        parent.add_component(component)

    def render(self):
        """Renders the current component as HTML.
        """
        if self.template:
            if self.remove_after_render:
                del self.parent._components[self.id]

            return render_to_string(self.template, {
                "self": self,
                "js": JSCreator(self, self.actions).create(),
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
