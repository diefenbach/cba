import json
import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from . utils import LazyEncoder
# from . utils import time_it

logger = logging.getLogger(__name__)
performance_logger = logging.getLogger("cba.peformance")


class CBAView(View):
    template = "cba/main.html"

    def __init__(self, **kwargs):
        super(CBAView, self).__init__(**kwargs)
        self.root = self.root("root")
        self._html = []
        self._messages = []

    def get(self, *args, **kwargs):
        # content = time_it(self.root.render, performance_logger, "Rendered in:")
        content = self.root.render()

        self.request.session["root"] = self.root

        return render(self.request, self.template, {
            "content": content,
        })

    def post(self, *args, **kwargs):
        # time_it(self._load_data, func_args=[self.root], logger=performance_logger, log_message="Loaded in:")
        root = self.request.session["root"]
        self._clear_components_data(root)
        self._load_data(root)

        handler = self.request.POST.get("handler")
        event_id = self.request.POST.get("event_id")
        component = root.get_component(event_id)

        # Bubbles up the components to find the handler
        while component:
            if hasattr(component, handler):
                component.event_id = event_id
                getattr(component, handler)()
                break
            component = component.parent

        self._collect_components_data(root)

        # logger.debug("Refreshed components: {}".format(self._html))
        self.request.session["root"] = root

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

    def _collect_components_data(self, root):
        """Collects refreshed html and messages from all components.
        """
        if root._html:
            self._html.append(root._html)

        if root._messages:
            self._messages.extend(root._messages)

        if hasattr(root, "components"):
            for component in root.components:
                if component._html:
                    self._html.append(component._html)
                if component._messages:
                    self._messages.extend(component._messages)
                self._collect_components_data(component)

    def _load_data(self, root):
        """Loads components with values from the browser.
        """
        if hasattr(root, "components"):
            for component in root.components:
                if component.id in self.request.POST:
                    root._components[component.id].value = self.request.POST.get(component.id)
                self._load_data(component)
