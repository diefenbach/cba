from . base import Component


class Button(Component):
    """A HTML button.

        handler
            The method which is called when the button is clicked.

        value
            The value of the button

    """
    template = "cba/components/button.html"

    def __init__(self, handler=None, value="", *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.handler = handler
        self.value = value


class Group(Component):
    """A simple group to group compontens together for easier refresh.
    """
    template = "cba/components/group.html"


class HiddenInput(Component):
    """Renders to a HTML input hidden tag.

        value
            The value of the hidden input field.
    """
    template = "cba/components/hidden_input.html"

    def __init__(self, value="", *args, **kwargs):
        super(HiddenInput, self).__init__(*args, **kwargs)
        self.value = value


class Image(Component):
    """Renders to a HTML img tag.

        src
            The url to the image file

    """
    template = "cba/components/image.html"

    def __init__(self, src, alt="", title="", *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)
        self.src = src
        self.alt = alt
        self.title = title


class Select(Component):
    template = "cba/components/select.html"

    def __init__(self, options, *args, **kwargs):
        super(Select, self).__init__(*args, **kwargs)
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

    def __init__(self, id, label=None, value="", rows=10, *args, **kwargs):
        super(TextArea, self).__init__(id, *args, **kwargs)
        self.label = label
        self.rows = rows
        self.value = value


class Text(Component):
    template = "cba/components/text.html"

    def __init__(self, id, value, *args, **kwargs):
        super(Text, self).__init__(id, *args, **kwargs)
        self.value = value


class TextInput(Component):
    template = "cba/components/text_input.html"

    def __init__(self, id, value="", label=None, error=None, *args, **kwargs):
        super(TextInput, self).__init__(id, *args, **kwargs)
        self.error = False
        self.label = label
        self.value = value
