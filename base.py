from collections import OrderedDict

from django.conf import settings
from django.template.loader import render_to_string

from . utils import JSCreator


class Component(object):
    """
        id
            The unique id of the compoment. This must be unique troughout the
            whole application.

        initial_components
            The initial sub components of this components

        attributes
            HTML attributes of the component
    """
    template = None

    def __init__(self, id, initial_components=None, attributes=None, css_class=None, actions=None, *args, **kwargs):
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

        self.load_components()

    def add_component(self, component):
        component.parent = self
        self._components[component.id] = component

    @property
    def components(self):
        return self._components.values()

    def get_component(self, id, direct_only=False):
        component = self._components.get(id)
        if component:
            return component
        elif direct_only is False:
            for component in self.components:
                temp = component.get_component(id, direct_only)
                if temp:
                    return temp

    def init_components(self):
        pass

    def load_components(self):
        """
        Loads the initial components into the default components structure.
        """
        for component in self.initial_components:
            self.add_component(component)
        self.initial_components = []

    def refresh(self):
        self._html = ["#{}".format(self.id), self.render()]

    def render(self):
        return render_to_string(self.template, {
            "self": self,
            "js": JSCreator(self, self.actions).create(),
        })
