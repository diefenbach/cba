import json

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View

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

    def __init__(self, id, initial_components=None, attributes=None, *args, **kwargs):
        self.id = id
        self.initial_components = initial_components or []
        self.attributes = attributes or {}

        self.html = None
        self.components = []
        self.components_dict = {}
        self.parent = None
        self.actions = kwargs.get("actions", [])
        self.html = None
        self.parent = None

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

    def after_init(self):
        pass

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


class CBAView(View):
    template = "cba/main.html"

    def __init__(self, **kwargs):
        super(View, self).__init__(**kwargs)
        self.root = self.root("root")
        self.html = []

    def load_components(self, root):
        """
        Loads components with values from the browser.
        """
        if hasattr(root, "components"):
            for component in root.components:
                if component.id in self.request.GET:
                    root.components_dict[component.id].value = self.request.GET.get(component.id)
                self.load_components(component)

    def collect_refreshed_components(self, root):
        """
        Collects the html from all components which should be refreshed.
        """
        if hasattr(root, "components"):
            for component in root.components:
                if component.html:
                    self.html.append(component.html)
                self.collect_refreshed_components(component)

    def get(self, *args, **kwargs):
        if self.request.is_ajax():
            self.load_components(self.root)

            handler = self.request.GET.get("handler")
            event_id = self.request.GET.get("event_id")
            component = self.root.get_component(event_id)

            # Bubbles up the components to find the handler
            while component:
                if hasattr(component, handler):
                    component.event_id = event_id
                    getattr(component, handler)()
                    break
                component = component.parent

            self.collect_refreshed_components(self.root)

            return HttpResponse(
                json.dumps({"html": self.html}),
                content_type='application/json'
            )
        else:
            self.root.after_init()
            return render(self.request, self.template, {
                "content": self.root.render()
            })
