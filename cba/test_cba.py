from cba import components


def test_hidden_input():
    hidden_input = components.HiddenInput(id="hidden-1")
    assert hidden_input.id == "hidden-1"
    assert hidden_input.value == ""


def test_hidden_input_with_value():
    hidden_input = components.HiddenInput(id="hidden-1", value="1")
    assert hidden_input.id == "hidden-1"
    assert hidden_input.value == "1"


def test_hidden_input_render():
    hidden_input = components.HiddenInput(id="hidden-1", value="1")
    html = hidden_input.render()

    expected_html = """
        <input class="component render"
               id="hidden-1"
               name="hidden-1"
               type="hidden"
               value="1" />
        """

    assert "".join(html.split()) == "".join(expected_html.split())


def test_button():
    button = components.Button(id="button-1")
    assert button.id == "button-1"
    assert button.value == ""


def test_button_with_value():
    button = components.Button(id="button-1", value="OK")
    assert button.id == "button-1"
    assert button.value == "OK"


def test_button_render():
    button = components.Button(id="button-1", value="OK")
    html = button.render()

    expected_html = """
        <button id="button-1"
                class="ui button render">
            OK
        </button>
    """
    assert "".join(html.split()) == "".join(expected_html.split())
