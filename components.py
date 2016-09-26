from . base import Component


class Button(Component):
    """A HTML button.

        default_ajax
            If set to true a click to the button will be processed by the
            default CBA ajax behaviour, which means the click event will be
            sent via a post Ajax call to the handler.

        handler
            The method which is called when the button is clicked.

        value
            The value of the button.
    """
    template = "cba/components/button.html"

    def __init__(self, value="", handler=None, default_ajax=True, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.value = value
        self.handler = handler
        self.default_ajax = default_ajax


class Group(Component):
    """A simple group component to arrange compontens together. For instance for
    styling reasons or to easier refresh its sub components.
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


class HTML(Component):
    """A HTML tag.

        tag
            The outer tag of the component.

        text
            The text of the component. Will be rendered within the outer tag.
    """
    template = "cba/components/html.html"

    def __init__(self, tag="div", text="", *args, **kwargs):
        super(HTML, self).__init__(*args, **kwargs)
        self.tag = tag
        self.text = text


class Image(Component):
    """A HTML image component.

        src
            The url to the image file.

        alt
            The content alt tag of the image file.

        title
            The content of the title tag of the image.

    """
    template = "cba/components/image.html"

    def __init__(self, src="", alt="", title="", *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)
        self.src = src
        self.alt = alt
        self.title = title


class Link(Component):
    """A HTML link.

        handler
            The method which is called when the button is clicked.

        text
            The content of the HTML tag.

        default_ajax
            If set to true a click to the button will be processed by the
            default CBA ajax behaviour, which means the click event will be
            sent via a post Ajax call to the handler.

    """
    template = "cba/components/link.html"

    def __init__(self, handler=None, text="", default_ajax=True, *args, **kwargs):
        super(Link, self).__init__(*args, **kwargs)
        self.default_ajax = default_ajax
        self.handler = handler
        self.text = text


class Menu(Component):
    """The root container of a pop up menu.
    """
    template = "cba/components/menu.html"

    def __init__(self, *args, **kwargs):
        super(Menu, self).__init__(*args, **kwargs)


class MenuItem(Component):
    """An item of a pop up menu.

        name
            The name of the menu item, which is displayed to the customer

        handler
            The method which is called when the button is clicked.

        default_ajax
            If set to true a click to the button will be processed by the
            default CBA ajax behaviour, which means the click event will be
            sent via a post Ajax call to the handler.

    """
    template = "cba/components/menu_item.html"

    def __init__(self, handler=None, href=None, name="", default_ajax=True, *args, **kwargs):
        super(MenuItem, self).__init__(*args, **kwargs)
        self.default_ajax = default_ajax
        self.handler = handler
        self.href = href
        self.name = name


class ConfirmModal(Component):
    """A convenient modal dialog with a yes and no button. When the dialog is
       answered with yes the handler method is called via an ajax request.

        event_id
            The event_id which is passed to the backend when the dialog has
            been approved.

        handler
            The method which is called when the dialog has been approved.

        header
            The header of the dialog which is displayed to the user.

        text
            The text of the dialog which is displayed to the user.
    """
    template = "cba/components/confirm_modal.html"
    remove_after_render = True

    def __init__(self, event_id, handler, header=None, text=None, *args, **kwargs):
        super(ConfirmModal, self).__init__(*args, **kwargs)
        self.text = text
        self.event_id = event_id
        self.handler = handler
        self.header = header


class Modal(Component):
    """A modal dialog.

        header
            The header of the dialog which is displayed to the user.

        close_button
            When set to True a close button is displayed.
    """
    template = "cba/components/modal.html"
    remove_after_render = True

    def __init__(self, header=None, close_button=True, *args, **kwargs):
        super(Modal, self).__init__(*args, **kwargs)
        self.header = header
        self.close_button = close_button


class Select(Component):
    """A HTML Select box.

        label
            An optional label for the select box.

        options
            Options which can be selected by the user.

        The current value (selected values) of the select box.
    """
    template = "cba/components/select.html"

    def __init__(self, id, label=None, value=None, options=None, multiple=False, *args, **kwargs):
        super(Select, self).__init__(id, *args, **kwargs)
        self.label = label
        self.multiple = multiple
        self.options = options or []
        self.value = value

    def get_names(self):
        """Returns the names of all selected options as a list.
        """
        names = []
        for option in self.options:
            if str(option["value"]) in self.values:
                self.names.append(option["name"])
        return names

    def clear(self):
        self.value = None


class Table(Component):
    """A HTML table

        columns
            A list of strings which represent the header of the table.

        data
            A list of list which represents the rows and columns of the table.
    """
    template = "cba/components/table.html"

    def __init__(self, columns, data=None, label=None, selected=None, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        self.columns = columns
        self.data = data or []
        self.label = label

    def add_row(self, data):
        """Adds a row to the table.

            data
                A list of items which is added to the table. The length must
                be commpliant to the list of columns.
        """
        temp = []
        for item in data:
            if isinstance(item, Component):
                self.add_component(item)
                temp.append(item.render())
            else:
                temp.append(item)
        self.data.append(temp)


class Tab(Component):
    """The container component for tab item.
    """
    template = "cba/components/tab.html"


class TabItem(Component):
    """A tab item.

        active
            If true the tab item is displayed.

        title
            The title of the tab item.
    """
    def __init__(self, title="", active=False, *args, **kwargs):
        super(TabItem, self).__init__(*args, **kwargs)
        self.active = active
        self.title = title


class TextArea(Component):
    """A HTML Textarea

        label
            The optional label of the text area.

        rows
            The amount of rows of the text area.
.
        value
            The current value of the text area.

        error
            The current validation error of the text area.
    """
    template = "cba/components/textarea.html"

    def __init__(self, label=None, value="", error=None, rows=10, *args, **kwargs):
        super(TextArea, self).__init__(*args, **kwargs)
        self.error = error
        self.label = label
        self.rows = rows
        self.value = value

    def clear(self):
        """Sets the value an error to empty strings..
        """
        self.value = ""
        self.error = ""


class TextInput(Component):
    """An HTML text input.

        error
            The current validation error of the text input.

        label
            The optional label of the text input.

        placeholder
            The optional placeholder of the text input. If given it is
            displayed within the input field.

        value
            The current value of the text input.
    """
    template = "cba/components/text_input.html"

    def __init__(self, id=None, value="", label=None, placeholder=None, error=None, *args, **kwargs):
        super(TextInput, self).__init__(id, *args, **kwargs)
        self.error = error
        self.label = label
        self.placeholder = placeholder
        self.value = value

    def clear(self):
        """Sets the value an error to empty strings.
        """
        self.error = ""
        self.value = ""
