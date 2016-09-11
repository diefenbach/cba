import logging
from collections import OrderedDict

from django.template.loader import render_to_string

from . utils import JSCreator

logger = logging.getLogger(__name__)


class Component(object):
    """A component is a part of a HTML application.
    """
    template = None

    def __init__(self, id, initial_components=None, attributes=None, css_class=None, actions=None, *args, **kwargs):
        """
            id
                The unique id of the compoment. This must be unique troughout the
                whole application.

            attributes
                HTML attributes of the component.

            css_class
                The css class of the component.

            initial_components
                The initial sub components of this components.

            template
                The path to the template which is used to render the component.
        """
        self.id = id
        self.initial_components = initial_components or []
        self.attributes = attributes or {}
        self.css_class = css_class

        self.actions = actions or []
        self._html = None
        self._components = OrderedDict()
        self.parent = None

        if initial_components:
            self.initial_components = initial_components
        else:
            self.init_components()

        self._adds_components()

    def add_component(self, component):
        """Adds the given component as sub component to the current component.

        component
            The component which is added to the current component
        """
        component.parent = self
        self._components[component.id] = component

    @property
    def components(self):
        """Returns all direct sub components of the current component as list.
        """
        return self._components.values()

    def get_component(self, id, direct_only=False):
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
                temp = component.get_component(id, direct_only)
                if temp:
                    return temp

    def init_components(self):
        """Can be overriden to set the initial sub components of the current
        components.
        """
        pass

    def refresh(self):
        """Rerenders the current component once the current request is returned
        to the browser.
        """
        self._html = ["#{}".format(self.id), self.render()]

    def render(self):
        """Renders the current component as HTML.
        """
        return render_to_string(self.template, {
            "self": self,
            "js": JSCreator(self, self.actions).create(),
        })

    def _adds_components(self):
        """Adds initial components into the default components structure.
        """
        if self.initial_components:
            logger.debug("Components loading for {}:".format(self.id))

        for component in self.initial_components:
            logger.debug("\t- {}".format(component.id))
            self.add_component(component)

        if self.initial_components:
            self.initial_components = []
