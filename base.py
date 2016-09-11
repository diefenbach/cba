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

    def __init__(self, id, initial_components=None, attributes=None, css_class=None, *args, **kwargs):
        self.id = id
        self.initial_components = initial_components or []
        self.attributes = attributes or {}
        self.css_class = css_class

        self.html = None
        self.components = []
        self.components_dict = {}
        self.parent = None
        self.actions = kwargs.get("actions", [])

        if initial_components is None:
            self.init_components()
        else:
            self.initial_components = initial_components

        self.load_components()

    def add_component(self, component):
        component.parent = self
        self.components_dict[component.id] = component
        self.components.append(component)

    def get_component(self, id, direct_only=False):
        for component in self.components:
            if component.id == id:
                return component
            if direct_only is False:
                temp = component.get_component(id)
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
        self.html = ["#{}".format(self.id), self.render()]

    def render(self):
        return render_to_string(self.template, {
            "self": self,
            "js": JSCreator(self, self.actions).create(),
        })
