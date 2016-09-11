from . base import Component


class Button(Component):
    template = "cba/components/button.html"

    def __init__(self, handler, value="", *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.handler = handler
        self.value = value


class Image(Component):
    template = "cba/components/image.html"

    def __init__(self, id, src, *args, **kwargs):
        super(Image, self).__init__(id, *args, **kwargs)
        self.src = src


class Page(Component):
    template = "cba/components/page.html"


class Text(Component):
    template = "cba/components/text.html"

    def __init__(self, id, value, *args, **kwargs):
        super(Text, self).__init__(id, *args, **kwargs)
        self.value = value


class TextInput(Component):
    template = "cba/components/text_input.html"

    def __init__(self, id, value="", label=None, *args, **kwargs):
        super(TextInput, self).__init__(id, *args, **kwargs)
        self.label = label
        self.value = value


class HiddenInput(TextInput):
    template = "cba/components/hidden_input.html"

    def __init__(self, id, value="", *args, **kwargs):
        super(HiddenInput, self).__init__(id, *args, **kwargs)
        self.value = value


class Select(Component):
    template = "cba/components/select.html"

    def __init__(self, id, options, actions=None, *args, **kwargs):
        super(Select, self).__init__(id)
        self.options = options

    def get_name(self):
        for option in self.options:
            if str(option["value"]) == self.value:
                return option["name"]


class Table(Component):
    template = "cba/components/table.html"

    def __init__(self, id, columns, data=None, *args, **kwargs):
        super(Table, self).__init__(id, *args, **kwargs)
        self.data = data or []
        self.columns = columns

    def add_data(self, data):
        temp = []
        for item in data:
            if isinstance(item, Component):
                self.add_component(item)
                temp.append(item.render())
            else:
                temp.append(item)
        self.data.append(temp)


class Tabs(Component):
    template = "cba/components/tabs.html"


class Tab(Component):
    def __init__(self, id, title, active=False, *args, **kwargs):
        super(Tab, self).__init__(id, *args, **kwargs)
        self.active = active
        self.title = title


class TextArea(Component):
    template = "cba/components/textarea.html"

    def __init__(self, id, label=None, value="", *args, **kwargs):
        super(TextArea, self).__init__(id, *args, **kwargs)
        self.label = label
        self.value = value


class SimpleLayout(Component):
    template = "cba/components/simple_layout.html"
